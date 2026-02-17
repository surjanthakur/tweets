from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.db_tables import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
import jwt

pass_hash = PasswordHash.recommended()


# hashed password
def get_hashed_password(password: str):
    return pass_hash.hash(password=password)


# verify password
def verify_password(plain_password: str, hash_password: str):
    return pass_hash.verify(plain_password, hash_password)


# create new account
async def create_account(form_data: object, db: AsyncSession):
    new_user = User(
        username=form_data.username,
        email=form_data.email,
        password=get_hashed_password(form_data.password),
    )
    try:
        db.add(new_user)
        await db.commit()
        return {"message": "signup succeeded"}

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )


# authenticate user
async def authenticate_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    pass
