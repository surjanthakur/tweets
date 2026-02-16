from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import Tweet
from sqlmodel import select
from sqlalchemy.orm import selectinload


# fetch tweets form db
async def get_tweets(db: AsyncSession):
    query = await db.exec(select(Tweet))
    return query.all()


# fetch tweet by id
async def tweet_by_id(tweet_id, db: AsyncSession):
    query = await db.exec(
        select(Tweet)
        .options(selectinload(Tweet.comments))
        .where(Tweet.tweet_id == tweet_id)
    )
    return query.first()
