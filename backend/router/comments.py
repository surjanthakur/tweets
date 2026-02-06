from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete, update
from sqlalchemy.orm import selectinload
from uuid import UUID
from db.db_tables import Comment, User, Tweet
from uuid import UUID
from typing import List
from auth.auth_service import get_current_user
from db.db_connection import get_session

comment_router = APIRouter(prefix="/comment", tags=["comments"])


@comment_router.post("/{tweet_id}create", status_code=status.HTTP_201_CREATED)
async def create_comment(
    tweet_id: UUID,
    curr_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if not curr_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="login first"
        )
    statement = await db.exec(select(Tweet).where(Tweet.tweet_id == tweet_id))
    my_tweet = statement.first()
    if not my_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tweet not found to add comment",
        )
    new_comment = Comment(tweet_id=my_tweet.tweet_id, user_id=curr_user.user_id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return {"message": "tweet created"}
