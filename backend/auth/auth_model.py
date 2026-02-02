from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class request_user(BaseModel):
    username: Annotated[
        str,
        Field(
            ...,
            title="@yourname field",
            min_length=3,
            max_length=40,
        ),
    ]
    email: Annotated[EmailStr, Field(..., title="email field")]
    password: Annotated[str, Field(..., min_length=4, title="password field")]


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    token: str
    token_type: str
