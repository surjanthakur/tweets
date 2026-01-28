from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.db_connection import get_session
from db.db_tables import User
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from bcrypt import checkpw

load_dotenv()


secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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
async def get_user_by_handle_name(
    handle_name: str,
    password: str,
    db: AsyncSession = Depends(get_session),
):
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
