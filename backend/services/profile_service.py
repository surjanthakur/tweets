from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from repository import profile_repo
from db.db_tables import Profile


# get currProfile
async def get_currProfile(user_id: str, db: AsyncSession):
    my_profile = await profile_repo.get_by_userId(user_id, db)

    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return my_profile


# create profile
async def create_profile(req_data, db: AsyncSession, user_id):
    exist_profile = await profile_repo.get_profile_only(user_id, db)
    if exist_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="profile already exist!"
        )
    new_profile = Profile(**req_data, user_id=user_id)
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


# update profile
async def update_profile(req_data, user_id, db: AsyncSession):
    my_profile = await profile_repo.get_profile_only(user_id, db)
    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="profile not found !"
        )
    updated_dict = req_data.model_dump(exclude_unset=True)
    for k, v in updated_dict:
        setattr(my_profile, k, v)
    db.add(my_profile)
    db.commit()
    return my_profile
