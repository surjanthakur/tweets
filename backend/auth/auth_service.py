from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from db.db_connection import get_session
from db.db_tables import User
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from bcrypt import checkpw, hashpw, gensalt
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from .pydantic_token import TokenData

load_dotenv()


secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# get hashed password
def get_hashed_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


# verify password and return true/false
async def verify_password(plain_pass: str, hash_pass: str) -> bool:
    try:
        return checkpw(
            password=plain_pass.encode("utf-8"),
            hashed_password=hash_pass.encode("utf-8"),
        )
    except ValueError:
        return False


# get user by handle name
async def get_user_by_handle_name(handle_name: str, password: str, db: AsyncSession):
    try:
        result = await db.exec(select(User).where(User.handle_name == handle_name))
        my_user = result.first()
        if not my_user:
            return False
        if not verify_password(password, my_user.password):
            return False
        return my_user
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {err}",
        )


# create access token and return it
def create_access_token(data: dict, expires_token_time: timedelta | None = None):
    user_data = data.copy()
    if expires_token_time:
        expire = datetime.now(timezone.utc) + expires_token_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    user_data.update({"exp": expire})
    access_token = jwt.encode(user_data, secret_key, algorithm=algorithm)
    return access_token


# get current user by access token
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        handle_name = payload.get("sub")
        if handle_name is None:
            raise credentials_exception
        token_data = TokenData(handle_name=handle_name)
    except InvalidTokenError:
        raise credentials_exception

    curr_user = get_user_by_handle_name(handle_name=token_data.handle_name, db=db)
    if curr_user in None:
        raise credentials_exception
    return curr_user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
