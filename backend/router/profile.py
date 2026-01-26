from sqlmodel.ext.asyncio.session import AsyncSession
from models.profile_model import request_profile, response_profile
from db.db_tables import Profile
from db.db_connection import get_session
import logging
from fastapi import APIRouter, HTTPException, status, Depends, Path
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
    curr_handle: str = Path(..., title="profile username name"),
    db: AsyncSession = Depends(get_session),
):
    try:
        result = await db.exec(
            select(Profile)
            .options(selectinload(Profile.tweets))
            .where(Profile.handle_name == curr_handle)
        )
        my_profile = result.first()
        if not my_profile:
            logger.warning(
                f"cant find profile with this profile handle name: {curr_handle}"
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
    "/create/{curr_username}",
    status_code=status.HTTP_201_CREATED,
    summary="Create profile for the authenticated user",
)
async def create_profile(
    profile_data: request_profile,
    curr_handle: str = Path(..., title="profile username name"),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(Profile).where(Profile.handle_name == curr_handle))
    my_profile = result.first()
    if my_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a profile. Only one profile per user allowed.",
        )
    try:
        new_profile = Profile(**profile_data.model_dump(exclude_unset=True))
        new_profile.handle_name = curr_handle
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=f"Profile {new_profile.name} created successfully.",
        )
    except Exception as err:
        logger.error(f"error while creating profile:{err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error while creating profile",
        )


# edit profile id user has a profile
@profile_router.put("/edit/{curr_username}")
async def edit_profile(
    profile_data: request_profile,
    curr_handle: str = Path(..., title="profile username"),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(Profile).where(Profile.handle_name == curr_handle))
    my_profile = result.first()
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
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f"Profile {my_profile.name} edited successfully.",
        )
    except Exception as err:
        logger.error(f"error while editing profile:{err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error while editing profile",
        )
