from sqlmodel.ext.asyncio.session import AsyncSession
from models.tweets_model import request_tweet, response_tweet
from db.db_tables import Tweet
from db.db_connection import get_session
import logging
from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

tweet_router = APIRouter(tags=["tweets"], prefix="/tweet")


async def get_tweet_db(db: AsyncSession, curr_tweet_id: UUID) -> Tweet | None:
    result = await db.exec(
        select(Tweet)
        .options(selectinload(Tweet.comments))
        .where(Tweet.tweet_id == curr_tweet_id)
    )
    return result.first()


# get all tweets
@tweet_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[response_tweet]
)
async def get_all_tweets(db: AsyncSession = Depends(get_session)):
    try:
        result = await db.exec(select(Tweet).options(selectinload(Tweet.profile)))
        tweets = result.all()
        if not tweets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No tweets found"
            )
        return tweets
    except Exception as err:
        logging.error(f"Error fetching tweets: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


# Get tweet by ID
@tweet_router.get("/{tweet_id}")
async def get_tweet_by_id(tweet_id: UUID, db: AsyncSession = Depends(get_session)):
    try:
        my_tweet = await get_tweet_db(db, tweet_id)
        if not my_tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
            )
        return my_tweet
    except Exception as err:
        logging.error(f"Error fetching tweet by ID: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@tweet_router.post("/create/{profile_id}")
def create_new_tweet(
    tweet_data: request_tweet, profile_id: UUID, db: AsyncSession = Depends(get_session)
):
    pass
