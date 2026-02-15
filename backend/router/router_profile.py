from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import Profile
from db.db_connection import get_session
from models.validation_models import RequestProfile, ResponseProfile
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from auth.auth_service import get_current_user
from db.db_tables import User
from ..services import profile_service

profile_router = APIRouter(prefix="/profiles", tags=["Profiles"])


# Get profile
@profile_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user's profile",
    response_model=ResponseProfile,
)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await profile_service.get_currProfile(user_id=current_user.user_id, db=db)


# create profile
@profile_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create profile for the authenticated user",
    response_model=ResponseProfile,
)
async def create_profile(
    req_data: RequestProfile,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await profile_service.create_profile(
        req_data=req_data, db=db, user_id=current_user.user_id
    )


# edit profile
@profile_router.put(
    "/edit",
    status_code=status.HTTP_200_OK,
    summary="Edit current user's profile",
)
async def edit_profile(
    profile_data: RequestProfile,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await profile_service.update_profile(
        req_data=profile_data,
        user_id=current_user.user_id,
        db=db,
    )
