from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import Profile
from db.db_connection import get_session
from models.validation_models import RequestProfile
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlalchemy.orm import selectinload
from auth.auth_service import get_current_user
from db.db_tables import User

profile_router = APIRouter(prefix="/profile", tags=["Profile"])


# Get profile
@profile_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user's profile",
)
async def get_profile(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        result = await db.exec(
            select(Profile)
            .options(selectinload(Profile.tweets))
            .where(Profile.user_id == current_user.user_id)
        )
        my_profile = result.first()
        if not my_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="cant find profile",
            )
        return my_profile
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error while getting profile: {err}",
        )


# create new profile
@profile_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create profile for the authenticated user",
)
async def create_profile(
    profile_data: RequestProfile,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        statement = await db.exec(
            select(Profile).where(Profile.user_id == current_user.user_id)
        )
        exist_pofile = statement.first()
        if exist_pofile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a profile. Only one profile per user allowed.",
            )
        new_profile = Profile(
            **profile_data.model_dump(exclude_unset=True), user_id=current_user.user_id
        )
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return new_profile
    except HTTPException:
        raise


# edit profile
@profile_router.put("/edit")
async def edit_profile(
    profile_data: RequestProfile,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    statement = await db.exec(
        select(Profile).where(Profile.user_id == current_user.user_id)
    )
    my_profile = statement.first()
    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a profile to edit.",
        )

    updated_dic = profile_data.model_dump(exclude_unset=True)
    for k, v in updated_dic.items():
        setattr(my_profile, k, v)
    try:
        db.add(my_profile)
        await db.commit()
        await db.refresh(my_profile)
        return my_profile
    except HTTPException:
        raise
