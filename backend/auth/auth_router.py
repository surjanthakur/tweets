from fastapi import APIRouter, HTTPException, status, Depends
from db.db_tables import User
from db.db_connection import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .pydantic_token import Token, request_user
from .auth_service import (
    create_access_token,
    get_user_by_handle_name,
    get_hashed_password,
)
from datetime import timedelta
from sqlmodel import select


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# create user
@auth_router.post("/register")
async def create_user(user_data: request_user, db: AsyncSession = Depends(get_session)):
    print("HANDLE:", user_data.handle_name)
    result = await db.exec(
        select(User).where(User.handle_name == user_data.handle_name)
    )
    exist_user = result.first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists",
        )
    hash_password = get_hashed_password(user_data.password)
    new_user = User(
        handle_name=user_data.handle_name,
        email=user_data.email,
        password=hash_password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.user_id}


# login the user
@auth_router.post("/login")
async def login_user_for_accessToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session_db: AsyncSession = Depends(get_session),
) -> Token:
    my_user = await get_user_by_handle_name(
        handle_name=form_data.username, password=form_data.password, db=session_db
    )
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials handle name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": my_user.handle_name}, expires_token_time=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
