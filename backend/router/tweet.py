from sqlmodel.ext.asyncio.session import AsyncSession
from models.tweets_model import request_tweet, response_tweet
from db.db_tables import Tweet, Profile
from db.db_connection import get_session
import logging
from fastapi import APIRouter, HTTPException, status, Depends
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
@tweet_router.get("/{tweet_id}", status_code=status.HTTP_200_OK)
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


# create new tweet
@tweet_router.post("/create/{curr_user_id}", status_code=status.HTTP_201_CREATED)
async def create_new_tweet(
    tweet_data: request_tweet,
    curr_user_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(Profile).where(Profile.user_id == curr_user_id))
    my_profile = result.first()
    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found for the user",
        )
    new_tweet = Tweet(**tweet_data.model_dump(exclude_unset=True))
    new_tweet.profile_id = my_profile.profile_id
    db.add(new_tweet)
    await db.commit()
    await db.refresh()
    return new_tweet


# delete tweet by id
@tweet_router.delete("/{tweet_id}/delete")
async def delete_tweet(tweet_id: UUID, db: AsyncSession = Depends(get_session)):
    my_tweet = get_tweet_db(db, tweet_id)
    if not my_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found",
        )
    await db.delete(my_tweet)
    await db.commit()
    return {"detail": "Tweet deleted successfully"}
