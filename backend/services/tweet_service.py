from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from repository.tweet_repo import get_tweets, tweet_by_id


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
    pass
