from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from repository.user_repo import get_user_by_email
from db.db_tables import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
import jwt

pass_hash = PasswordHash()


# get hashed password
def get_hashed_password(password: str):
    return pass_hash.hash(password=password)


# verify password
def verify_password(plain_password: str, hash_password: str):
    return pass_hash.verify(plain_password, hash_password)


# create new account
async def create_account(form_data, db: AsyncSession):
    user = await get_user_by_email(email=form_data.email, db=db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already exists"
        )
    hashed_password = ""
    new_user = User(
        username=form_data.username, email=form_data.email, password=form_data.password
    )
