from db.db_tables import User
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_user(username: str, db: AsyncSession):
    query = await db.exec(select(User).where(User.username == username))
    return query.first()
