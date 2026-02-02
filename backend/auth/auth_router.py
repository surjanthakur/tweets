from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from db.db_tables import User
from db.db_connection import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .auth_model import request_user
from .auth_service import (
    create_access_token,
    Authenticate_user,
    get_hashed_password,
    get_current_user,
)
from datetime import timedelta, timezone, datetime
from sqlmodel import select


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# login the user
@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, summary=" login user and get access token"
)
async def login_user_for_accessToken(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session_db: AsyncSession = Depends(get_session),
):
    my_user = await Authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=session_db,
    )
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials handle name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": my_user.username},
        expires_token_time=access_token_expires,
    )

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "login user successfully",
            "user": {
                "username": my_user.username,
                "email": my_user.email,
            },
        },
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        expires=access_token_expires,
        secure=False,
        path="/",
    )
    print(f"response cookies: {response}")
    return response


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
@auth_router.get("/current", status_code=status.HTTP_200_OK)
async def current_user(user: Annotated[User, Depends(get_current_user)]):
    print(f"current user: {user}")
    return user


# logout user
@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user():
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Logout successful"}
    )
    response.delete_cookie(
        key="access_token",
        httponly=True,
    )
    return response
