from sqlmodel.ext.asyncio.session import AsyncSession
from models.profile_model import request_profile, response_profile
from db.profile_table import Profile
from db.db_connection import get_session
import logging
from fastapi import APIRouter, HTTPException, status, Depends, Path
from uuid import UUID
from sqlmodel import select
from sqlalchemy.orm import selectinload
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

profile_router = APIRouter(prefix="/profile", tags=["Profile"])


# Get profile by handle name
@profile_router.get(
    "/{curr_username}", status_code=status.HTTP_200_OK, response_model=response_profile
)
async def get_profile(
    curr_username: str = Path(..., title="profile username name"),
    db: AsyncSession = Depends(get_session),
):
    try:
        result = await db.exec(
            select(Profile)
            .options(selectinload(Profile.tweets))
            .where(Profile. == handle_name)
        )
        my_profile = result.first()
        if not my_profile:
            logger.warning(
                f"cant find profile with this profile handle name: {handle_name}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="cant find profile with this profile handle name",
            )
        return my_profile
    except Exception as err:
        logger.error(f"error while getting profile: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error while getting profile",
        )


# create new_post if user authenticated
@profile_router.post(
    "/create/{user_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Create profile for the authenticated user",
)
async def create_profile(
    profile_data: request_profile,
    user_id: UUID = Path(..., title="user id field"),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(Profile).where(Profile.user_id == user_id))
    my_profile = result.first()
    if my_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a profile. Only one profile per user allowed.",
        )
    try:
        new_profile = Profile(**profile_data.model_dump(exclude_unset=True))
        new_profile.user_id = user_id
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=f"Profile {new_profile.handle_name} created successfully.",
        )
    except Exception as err:
        logger.error(f"error while creating profile:{err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error while creating profile",
        )


@profile_router.put("/edit/{handle_name}")
def edit_profile( handle_name: str = Path(..., title="profile handle name"),
    db: AsyncSession = Depends(get_session))