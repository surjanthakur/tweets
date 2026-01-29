from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List, Optional
from pydantic import field_validator
import uuid
from uuid import UUID
from datetime import datetime


# =========================
# User table
# =========================
class User(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True, default_factory=uuid.uuid4, nullable=False)
    username: Annotated[
        str,
        Field(
            ...,
            title="username field @yourname",
            min_length=3,
            max_length=40,
            unique=True,
            index=True,
        ),
    ]
    email: Annotated[str, Field(..., title="email field", unique=True, index=True)]
    password: Annotated[str, Field(..., title="hashed password field")]
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )
    profile: "Profile" = Relationship(back_populates="user")

    @field_validator("email", mode="before")
    @classmethod
    def email_validator(cls, value: str):
        if "@" not in value:
            raise ValueError("invalid email format")
        if value.split("@")[-1].lower() != "gmail.com":
            raise ValueError("email must end with gmail.com")
        return value

    @field_validator("username", mode="after")
    @classmethod
    def handle_validator(cls, value: str):
        if not value.startswith("@"):
            raise ValueError("username must start with @")
        return value


# =========================
# Profile table
# =========================
class Profile(SQLModel, table=True):
    profile_id: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    user_id: UUID = Field(
        foreign_key="user.user_id",
        nullable=False,
        unique=True,
        ondelete="CASCADE",
    )

    name: Annotated[str, Field(..., min_length=3, max_length=30)]
    profession: Annotated[str, Field(..., min_length=3, max_length=50)]
    location: Annotated[str, Field(..., min_length=3, max_length=100)]
    bio: Annotated[str, Field(..., min_length=10, max_length=350)]

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    user: "User" = Relationship(back_populates="profile")
    tweets: List["Tweet"] = Relationship(back_populates="profile")


# =========================
# Tweet table
# =========================
class Tweet(SQLModel, table=True):
    tweet_id: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    profile_id: UUID = Field(
        foreign_key="profile.profile_id",
        nullable=False,
        ondelete="CASCADE",
    )

    content: Annotated[str, Field(..., min_length=10, max_length=750)]

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    profile: "Profile" = Relationship(back_populates="tweets")
    comments: List["Comment"] = Relationship(back_populates="tweet")


# =========================
# Comment table
# =========================
class Comment(SQLModel, table=True):
    comment_id: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    tweet_id: UUID = Field(
        foreign_key="tweet.tweet_id",
        nullable=False,
        ondelete="CASCADE",
    )

    user_id: UUID = Field(
        foreign_key="user.user_id",
        nullable=False,
        ondelete="CASCADE",
    )

    content: Annotated[str, Field(..., min_length=1, max_length=150)]

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )
    tweet: "Tweet" = Relationship(back_populates="comments")
