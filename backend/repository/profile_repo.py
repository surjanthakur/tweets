from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from db.db_tables import Profile


# get profile by user id
async def get_by_userId(user_id: str, db: AsyncSession):
    query = await db.exec(
        select(Profile)
        .options(selectinload(Profile.tweets))
        .where(Profile.user_id == user_id)
    )
    return query.first()
