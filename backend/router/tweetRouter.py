from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import Tweet, Profile, User
from db.db_connection import get_session
from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from typing import List
from models.validation_models import RequestTweet, ResponseTweet
from auth.auth_service import get_current_user
from services.tweet_service import all_tweets, get_tweets_by_id, create_tweet

tweet_router = APIRouter(tags=["tweets"], prefix="/tweets")


# get all tweets
@tweet_router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[ResponseTweet],
    summary="Get all tweets",
)
async def get_all_tweets(session_db: AsyncSession = Depends(get_session)):
    return await all_tweets(db=session_db)


# Get tweet
@tweet_router.get(
    "/{tweet_id}", status_code=status.HTTP_200_OK, summary="Get tweet by ID"
)
async def get_tweet_by_id(
    tweet_id: UUID, session_db: AsyncSession = Depends(get_session)
):
    return await get_tweets_by_id(tweet_id=tweet_id, db=session_db)


# create tweet
@tweet_router.post(
    "/create", status_code=status.HTTP_201_CREATED, summary="Create a new tweet"
)
async def create_new_tweet(
    tweet_data: RequestTweet,
    current_user: User = Depends(get_current_user),
    session_db: AsyncSession = Depends(get_session),
):
    return await create_tweet(
        req_data=tweet_data.content, user_id=current_user.user_id, db=session_db
    )


# delete tweet
@tweet_router.delete(
    "/{tweet_id}/delete", status_code=status.HTTP_200_OK, summary="Delete a tweet"
)
async def delete_tweet(
    tweet_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    pass
