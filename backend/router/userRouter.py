from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from db.db_connection import get_session
from ..models.auth_models import User_validation


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/signup")
def create_account(
    req_form: User_validation, session_db: AsyncSession = Depends(get_session)
):
    pass
