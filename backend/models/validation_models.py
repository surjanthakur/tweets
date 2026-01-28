from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated


class RequestProfile(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    profession: Annotated[str, Field(min_length=3, max_length=30)]
    location: Annotated[str, Field(min_length=3, max_length=50)]
    bio: Annotated[str, Field(min_length=10, max_length=150)]
    profile_picture: HttpUrl

    class Config:
        from_attributes = True


class RequestTweet(BaseModel):
    content: Annotated[str, Field(min_length=10, max_length=250)]

    class Config:
        from_attributes = True
