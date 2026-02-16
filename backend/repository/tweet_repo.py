from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import Tweet
from sqlmodel import select
from sqlalchemy.orm import selectinload


# fetch tweets form db
async def get_tweets(db: AsyncSession):
    query = await db.exec(select(Tweet))
    return query.all()


async def tweet_by_id(tweet_id, db):
    pass
