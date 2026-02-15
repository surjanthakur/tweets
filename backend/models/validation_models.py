from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Annotated, Optional, List


class CommentValidation(BaseModel):
    content: Annotated[str, Field(..., min_length=10, max_length=750)]


class RequestProfile(BaseModel):
    """ptofile req form validation"""

    name: Annotated[str, Field(..., min_length=3, max_length=30)]
    profession: Annotated[str, Field(..., min_length=3, max_length=50)]
    bio: Annotated[str, Field(..., min_length=10, max_length=350)]
    location: Optional[Annotated[str, Field(..., min_length=3, max_length=100)]]

    class Config:
        from_attributes = True


class ResponseTweet(BaseModel):
    """Tweet fields for API response (no profile/comments to avoid circular refs)."""

    tweet_id: UUID
    content: str
    created_at: datetime
    profile: RequestProfile
    comments: List[CommentValidation] = []

    class Config:
        from_attributes = True


class RequestTweet(BaseModel):
    """tweet req form validation"""

    content: Annotated[str, Field(..., min_length=10, max_length=750)]

    class Config:
        from_attributes = True


class ResponseProfile(BaseModel):
    """Profile + tweets for API response (no user relationship to avoid circular refs)."""

    profile_id: UUID
    user_id: UUID
    name: str
    profession: str
    location: str
    bio: str
    created_at: datetime
    tweets: List[ResponseTweet] = []

    class Config:
        from_attributes = True
