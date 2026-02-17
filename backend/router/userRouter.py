from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from db.db_connection import get_session
from models.auth_models import User_validation
from services.auth_service import create_account, authenticate_user


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/signup")
async def signup_account(
    req_form: User_validation, session_db: AsyncSession = Depends(get_session)
):
    return await create_account(form_data=req_form, db=session_db)


@user_router.post("/login")
async def login_account(
    req_form: OAuth2PasswordRequestForm = Depends(),
    session_db: AsyncSession = Depends(get_session),
):
    return await authenticate_user(form_data=req_form, db=session_db)
