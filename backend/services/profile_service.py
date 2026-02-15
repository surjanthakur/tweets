from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from repository import profile_repo


# get currProfile
async def get_currProfile(user_id: str, db: AsyncSession):
    my_profile = await profile_repo.get_by_userId(user_id, db)

    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return my_profile
