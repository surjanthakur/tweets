from db.db_tables import User
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_user_by_email(email: str, db: AsyncSession):
    query = await db.exec(select(User).where(User.email == email))
    return query.first()
