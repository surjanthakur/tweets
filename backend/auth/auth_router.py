from fastapi import APIRouter, HTTPException, status, Depends
from db.db_tables import User
from db.db_connection import get_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .pydantic_token import Token
from .auth_service import create_access_token, get_user_by_handle_name
from datetime import timedelta


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# login the user
@auth_router.post("/login")
async def login_user_for_accessToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session),
) -> Token:
    my_user = await get_user_by_handle_name(
        handle_name=form_data.username, password=form_data.password
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
