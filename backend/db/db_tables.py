from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List
from pydantic import field_validator
import uuid
from datetime import date


# User table definition with validations
class User(SQLModel, table=True):
    user_id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            primary_key=True,
            nullable=False,
        ),
    ]
    username: Annotated[
        str, Field(..., title="username field", min_length=3, max_length=40)
    ]
    email: Annotated[str, Field(..., title="email field")]
    password: Annotated[str, Field(..., title="password field")]
    created_at: Annotated[
        date, Field(default_factory=date.today, title="created at field")
    ]

    #  email validator to check if email ends with gmail.com.
    @field_validator("email", mode="before")
    @classmethod
    def email_validator(clas, value):
        valid_email = value.split("@")[-1]
        if valid_email != "gmail.com":
            raise ValueError("not a valid email it should be [gmail.com]")
        return value


# Profile table definition with validations
class Profile(SQLModel, table=True):
    profile_id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            primary_key=True,
            nullable=False,
        ),
    ]
    user_id: Annotated[
        str,
        Field(
            foreign_key="user.user_id",
            nullable=False,
            title="user id field",
            ondelete="CASCADE",
        ),
    ]
    handle_name: Annotated[
        str,
        Field(
            ...,
            title="handlename field @yourname",
            min_length=3,
            max_length=30,
        ),
    ]
    profession: Annotated[
        str, Field(..., title="profession field", min_length=3, max_length=30)
    ]
    bio: Annotated[str, Field(..., title="bio field", min_length=10, max_length=150)]
    profile_picture: Annotated[str, Field(..., title="profile picture field")]
    tweets: List["Tweet"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    created_at: Annotated[
        date, Field(default_factory=date.today, title="created at field")
    ]

    # validator to check if handle_name  start with @.
    @field_validator("handle_name", mode="before")
    @classmethod
    def handle_validator(clas, value):
        if value.startswith("@"):
            return value
        raise ValueError("enter a valid handle name that start's with @yourname")

    # return title cased profession and bio.
    @field_validator("profession", "bio", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()


# Tweet table definition with validations
class Tweet(SQLModel, table=True):
    tweet_id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            primary_key=True,
            nullable=False,
        ),
    ]
    profile_id: Annotated[
        str,
        Field(
            foreign_key="profile.profile_id",
            nullable=False,
            title="profile id field",
            ondelete="CASCADE",
        ),
    ]
    content: Annotated[
        str, Field(..., title="content field", min_length=10, max_length=250)
    ]
    profile: "Profile" = Relationship(
        back_populates="tweets",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    created_at: Annotated[
        date, Field(default_factory=date.today, title="created at field")
    ]

    # return title cased content.
    @field_validator("content", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()
