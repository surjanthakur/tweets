from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from repository.tweet_repo import get_tweets, tweet_by_id
from repository.profile_repo import get_profile_only
from db.db_tables import Tweet


# get all tweets
async def all_tweets(db: AsyncSession):
    tweets = await get_tweets(db=db)
    if not tweets:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="tweets are empty!"
        )
    return tweets


# get tweet by id
async def get_tweets_by_id(tweet_id, db):
    my_tweet = await tweet_by_id(tweet_id=tweet_id, db=db)
    if not my_tweet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="tweet not found!"
        )
    return my_tweet


# create tweet
async def create_tweet(req_data, user_id, db):
    profile = await get_profile_only(user_id=user_id, db=db)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="profile not found!"
        )

    new_tweet = Tweet(content=req_data, profile_id=profile.profile_id)
    db.add(new_tweet)
    await db.commit()
    await db.refresh(new_tweet)
    return new_tweet
