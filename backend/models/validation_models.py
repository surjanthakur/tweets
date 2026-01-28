from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Optional


class RequestProfile(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=30)]
    profession: Annotated[str, Field(..., min_length=3, max_length=50)]
    location: Annotated[str, Field(..., min_length=3, max_length=100)]
    bio: Annotated[str, Field(..., min_length=10, max_length=350)]

    class Config:
        from_attributes = True


class RequestTweet(BaseModel):
    content: Annotated[str, Field(..., min_length=10, max_length=250)]

    class Config:
        from_attributes = True
