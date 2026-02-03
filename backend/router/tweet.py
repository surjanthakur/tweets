from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import Tweet, Profile, User, Like
from db.db_connection import get_session
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, update, delete
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List
from models.validation_models import RequestTweet, TweetResponse
from auth.auth_service import get_current_user

tweet_router = APIRouter(tags=["tweets"], prefix="/tweet")


# get all tweets
@tweet_router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[TweetResponse],
    summary="Get all tweets",
)
async def get_all_tweets(db: AsyncSession = Depends(get_session)):
    try:
        statement = await db.exec(select(Tweet).options(selectinload(Tweet.profile)))
        all_tweets = statement.all()
        return all_tweets if all_tweets else []
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {err}",
        )


# Get tweet by ID
@tweet_router.get(
    "/{tweet_id}", status_code=status.HTTP_200_OK, summary="Get tweet by ID"
)
async def get_tweet_by_id(tweet_id: UUID, db: AsyncSession = Depends(get_session)):
    try:
        statement = await db.exec(
            select(Tweet)
            .options(selectinload(Tweet.comments))
            .options(selectinload(Tweet.profile))
            .where(Tweet.tweet_id == tweet_id)
        )
        my_tweet = statement.first()
        if not my_tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
            )
        return my_tweet
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {err}",
        )


# create new tweet
@tweet_router.post(
    "/create", status_code=status.HTTP_201_CREATED, summary="Create a new tweet"
)
async def create_new_tweet(
    tweet_data: RequestTweet,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    try:
        statement = await db.exec(
            select(Profile).where(Profile.user_id == current_user.user_id)
        )
        my_profile = statement.first()
        if not my_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found create it first",
            )
        new_tweet = Tweet(content=tweet_data.content, profile_id=my_profile.profile_id)
        db.add(new_tweet)
        await db.commit()
        await db.refresh(new_tweet)
        return new_tweet
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {err}",
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
    try:
        statement = await db.exec(
            select(Tweet)
            .options(selectinload(Tweet.profile))
            .where(Tweet.tweet_id == tweet_id)
        )
        my_tweet = statement.first()
        if not my_tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tweet not found",
            )
        if not my_tweet.profile.user_id == current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this tweet",
            )
        await db.delete(my_tweet)
        await db.commit()
        return {"detail": "Tweet deleted successfully"}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {err}",
        )


# like count logic ---------------------------------------------->


@tweet_router.post("/{tweet_id}/like")
async def like_tweet(
    tweet_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    statement = await db.exec(
        select(Like).where(
            Like.user_id == current_user.user_id,
            Like.tweet_id == tweet_id,
        )
    )
    exist_like = statement.first()
    if exist_like:
        db.delete(exist_like)
        await db.exec(
            update(Tweet)
            .where(Tweet.tweet_id == tweet_id)
            .values(like_count=Tweet.like_count - 1)
        )
        db.commit()
        return {"message": "unliked", "liked": False}
    else:
        new_like = Like(tweet_id == tweet_id, user_id=current_user.user_id)
        db.add(new_like)
        await db.exec(
            update(Tweet)
            .where(Tweet.tweet_id == tweet_id)
            .values(lke_count=Tweet.like_count + 1)
        )
    db.commit()
    return {"message": "liked", "liked": True}
