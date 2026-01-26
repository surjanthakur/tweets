from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated
from .tweets_model import response_tweet


# Pydantic model for profile creation request
class request_profile(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            title="name field",
            min_length=3,
            max_length=30,
        ),
    ]
    profession: Annotated[str, Field(..., min_length=3, max_length=30)]
    bio: Annotated[str, Field(..., title="bio field", min_length=10, max_length=150)]
    profile_picture: Annotated[AnyUrl, Field(title="profile picture field")]


# Pydantic model for profile response
class response_profile(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            title="name field",
            min_length=3,
            max_length=30,
        ),
    ]
    bio: Annotated[str, Field(..., title="bio field", min_length=10, max_length=150)]
    profession: Annotated[str, Field(..., min_length=3, max_length=30)]
    profile_picture: Annotated[AnyUrl, Field(title="profile picture field")]
    followers_count: Annotated[int, Field(title="number of followers")]
    following_count: Annotated[int, Field(title="number of following")]
    created_at: Annotated[str, Field(..., title="created at field")]
    tweets: list[response_tweet]
