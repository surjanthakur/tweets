from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.db_tables import User
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from models.auth_models import Token
import jwt
from repository.user_repo import get_user
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    db_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="allow",
    )


setting = Settings()

pass_hash = PasswordHash.recommended()


# hashed password
def get_hashed_password(password: str):
    return pass_hash.hash(password=password)


# verify password
def verify_password(plain_password: str, hash_password: str):
    return pass_hash.verify(plain_password, hash_password)


# create access_token
def create_access_token(user_data: dict, expires_delta: timedelta | None = None):
    data_incode = user_data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    data_incode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_incode, setting.secret_key, algorithm=setting.algorithm
    )
    return encoded_jwt


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
async def authenticate_user(username: str, password: str, db: AsyncSession):
    my_user = await get_user(username=username, db=db)
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(plain_password=password, hash_password=my_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        user_data={"sub": username}, expires_delta=access_token_expires
    )
