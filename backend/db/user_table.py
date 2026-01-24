from sqlmodel import SQLModel, Field
from typing import Annotated
from pydantic import field_validator
import uuid
from uuid import UUID
from datetime import datetime


# User table definition with validations
class User(SQLModel, table=True):
    user_id: Annotated[
        UUID,
        Field(
            default_factory=lambda: uuid.uuid4(),
            primary_key=True,
            nullable=False,
        ),
    ]
    username: Annotated[
        str, Field(..., title="username field", min_length=3, max_length=40)
    ]
    email: Annotated[str, Field(..., title="email field")]
    password: Annotated[str, Field(..., title="password field")]
    created_at: datetime = Field(
        default_factory=datetime.now(datetime.utcnow), nullable=False
    )

    #  email validator to check if email ends with gmail.com.
    @field_validator("email", mode="before")
    @classmethod
    def email_validator(clas, value):
        valid_email = value.split("@")[-1]
        if valid_email != "gmail.com":
            raise ValueError("not a valid email it should be [gmail.com]")
        return value
