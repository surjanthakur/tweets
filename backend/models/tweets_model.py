from pydantic import BaseModel, EmailStr, Field, AnyUrl
from typing import Optional, Annotated


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
    created_at: Annotated[str, Field(..., title="created at field")]
