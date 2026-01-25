from pydantic import BaseModel, EmailStr, Field, AnyUrl
from typing import Optional, Annotated


# Pydantic model for user creation request
class request_user(BaseModel):
    username: Annotated[
        str,
        Field(
            ...,
            title="@username field",
            min_length=3,
            max_length=40,
        ),
    ]
    email: Annotated[EmailStr, Field(..., title="email field")]
    password: Annotated[str, Field(..., title="password field")]
