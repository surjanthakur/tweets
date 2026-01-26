from pydantic import BaseModel, Field
from typing import Annotated
from .profile_model import response_profile


# Pydantic model for tweet creation request.
class request_tweet(BaseModel):
    content: Annotated[
        str, Field(..., title="content field", min_length=10, max_length=250)
    ]


# Pydantic model for tweet response.
class response_tweet(BaseModel):
    content: Annotated[
        str, Field(..., title="content field", min_length=10, max_length=250)
    ]
    profile: response_profile
    created_at: Annotated[str, Field(..., title="created at field")]
