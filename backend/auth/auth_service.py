from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from db.db_connection import get_session
from db.db_tables import User
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from .auth_model import TokenData

load_dotenv()


secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
password_hash = PasswordHash.recommended()


# get hashed password
def get_hashed_password(password: str) -> str:
    return password_hash.hash(password=password)


# verify password and return true/false
def verify_password(plain_pass: str, hash_pass: str) -> bool:
    try:
        return password_hash.verify(password=plain_pass, hash=hash_pass)
    except ValueError:
        return False


# authenticate user
async def Authenticate_user(
    username: str, password: str, db: AsyncSession = Depends(get_session)
):
    try:
        result = await db.exec(select(User).where(User.username == username))
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
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    statement = await db.exec(select(User).where(User.username == token_data.username))
    curr_user = statement.first()
    if not curr_user:
        raise credentials_exception
    return curr_user
