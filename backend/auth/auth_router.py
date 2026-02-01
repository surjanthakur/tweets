from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from db.db_tables import User
from db.db_connection import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .auth_model import Token, request_user
from .auth_service import (
    create_access_token,
    Authenticate_user,
    get_hashed_password,
    get_current_user,
)
from datetime import timedelta
from sqlmodel import select


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# login the user
@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, summary=" login user and get access token"
)
async def login_user_for_accessToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session_db: AsyncSession = Depends(get_session),
) -> Token:
    my_user = await Authenticate_user(
        username=form_data.username, password=form_data.password, db=session_db
    )
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials handle name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": my_user.username},
        expires_token_time=access_token_expires,
    )
    Response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=2000,
        samesite="lax",
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="login user successfully"
    )


# create user
@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, summary="Register a new user"
)
async def create_user(user_data: request_user, db: AsyncSession = Depends(get_session)):
    result = await db.exec(select(User).where(User.email == user_data.email))
    exist_user = result.first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists",
        )
    hash_password = get_hashed_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# get current user
@auth_router.get(
    "/current",
    status_code=status.HTTP_200_OK,
    summary="return current user details with the access_token",
)
async def current_user(user: Annotated[User, Depends(get_current_user)]):
    return user
