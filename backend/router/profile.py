from sqlmodel.ext.asyncio.session import AsyncSession
from models.profile_model import request_profile, response_profile
from db.profile_table import Profile
from db.db_connection import get_session
import logging
from fastapi import APIRouter, HTTPException, status, Depends, Path
from uuid import UUID
from sqlmodel import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

profile_router = APIRouter(prefix="/profile", tags=["Profile"])


# Get profile by handle name
@profile_router.get(
    "/{handle_name}", status_code=status.HTTP_200_OK, response_model=response_profile
)
async def get_profile(
    handle_name: str = Path(..., title="profile handle name"),
    db: AsyncSession = Depends(get_session),
):
    try:
        result = await db.exec(
            select(Profile)
            .options(selectinload(Profile.tweets))
            .where(Profile.handle_name == handle_name)
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
            detail=f"error while getting profile: {err}",
        )
