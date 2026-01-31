from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Optional, List


class RequestProfile(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=30)]
    profession: Annotated[str, Field(..., min_length=3, max_length=50)]
    location: Annotated[str, Field(..., min_length=3, max_length=100)]
    bio: Annotated[str, Field(..., min_length=10, max_length=350)]

    class Config:
        from_attributes = True


class TweetResponse(BaseModel):
    """Tweet fields for API response (no profile/comments to avoid circular refs)."""

    tweet_id: UUID
    content: str
    created_at: datetime
    profile: RequestProfile

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    """Profile + tweets for API response (no user relationship to avoid circular refs)."""

    profile_id: UUID
    user_id: UUID
    name: str
    profession: str
    location: str
    bio: str
    created_at: datetime
    tweets: List[TweetResponse] = []

    class Config:
        from_attributes = True


class RequestTweet(BaseModel):
    content: Annotated[str, Field(..., min_length=10, max_length=750)]

    class Config:
        from_attributes = True
