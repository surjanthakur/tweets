from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List
from pydantic import field_validator
import uuid
from uuid import UUID
from datetime import datetime


# User table definition with validations
class User(SQLModel, table=True):
    user_id: Annotated[
        UUID,
        Field(default_factory=lambda: uuid.uuid4(), nullable=False),
    ]
    handle_name: Annotated[
        str,
        Field(
            ...,
            title="username field @yourname",
            primary_key=True,
            min_length=3,
            max_length=40,
            unique=True,
        ),
    ]
    email: Annotated[str, Field(..., title="email field")]
    password: Annotated[str, Field(..., title="password field")]
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    #  email validator to check if email ends with gmail.com.
    @field_validator("email", mode="before")
    @classmethod
    def email_validator(clas, value):
        valid_email = value.split("@")[-1]
        if valid_email != "gmail.com":
            raise ValueError("not a valid email it should be [gmail.com]")
        return value

    # validator to check if handle_name  start with @.
    @field_validator("handle_name", mode="before")
    @classmethod
    def handle_validator(clas, value):
        if value.startswith("@"):
            return value
        raise ValueError("enter a valid handle name that start's with @yourname")


# Profile table definition with validations
class Profile(SQLModel, table=True):
    profile_id: Annotated[
        UUID,
        Field(
            default_factory=lambda: uuid.uuid4(),
            primary_key=True,
            nullable=False,
        ),
    ]
    handle_name: Annotated[
        str,
        Field(
            foreign_key="user.handle_name",
            nullable=False,
            title="username field @yourname",
            ondelete="CASCADE",
            unique=True,
        ),
    ]
    name: Annotated[
        str,
        Field(
            ...,
            title=" name field",
            min_length=3,
            max_length=30,
        ),
    ]
    profession: Annotated[
        str, Field(..., title="profession field", min_length=3, max_length=30)
    ]
    bio: Annotated[str, Field(..., title="bio field", min_length=10, max_length=150)]
    profile_picture: Annotated[str, Field(..., title="profile picture field")]
    tweets: List["Tweet"] = Relationship(  # type: ignore
        back_populates="profile",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # return title cased profession and bio.
    @field_validator("profession", "bio", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()


# Tweet table definition with validations
class Tweet(SQLModel, table=True):
    tweet_id: Annotated[
        UUID,
        Field(
            default_factory=lambda: uuid.uuid4(),
            primary_key=True,
            nullable=False,
        ),
    ]
    profile_id: Annotated[
        UUID,
        Field(
            foreign_key="profile.profile_id",
            nullable=False,
            title="profile id field",
            ondelete="CASCADE",
        ),
    ]
    like_count: Annotated[int, Field(title="number of likes", default=0)]
    unlike_count: Annotated[int, Field(title="number of unlike", default=0)]
    content: Annotated[
        str, Field(..., title="content field", min_length=10, max_length=250)
    ]
    profile: "Profile" = Relationship(  # type: ignore
        back_populates="tweets",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    comments: List["Comment"] = Relationship(back_populates="tweet")
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # return title cased content.
    @field_validator("content", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()


# Comment table definition with validations ------------------------------>
class Comment(SQLModel, table=True):
    comment_id: Annotated[
        UUID,
        Field(
            default_factory=lambda: uuid.uuid4(),
            primary_key=True,
            nullable=False,
        ),
    ]
    tweet_id: Annotated[
        UUID,
        Field(
            foreign_key="tweet.tweet_id",
            nullable=False,
            title="tweet id field",
            ondelete="CASCADE",
        ),
    ]
    handle_name: Annotated[
        str,
        Field(
            foreign_key="user.handle_name",
            nullable=False,
            title="username field @yourname",
            ondelete="CASCADE",
            unique=True,
        ),
    ]
    tweet: "Tweet" = Relationship(back_populates="comments")
    content: Annotated[
        str, Field(..., title="comment content field", min_length=1, max_length=150)
    ]
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # return title cased content.
    @field_validator("content", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()
