from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List
from pydantic import field_validator
import uuid
from uuid import UUID
from datetime import datetime
from .profile_table import Profile


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
    profile: "Profile" = Relationship(
        back_populates="tweets",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    comments: List["Comment"] = Relationship(back_populates="tweet")
    created_at: datetime = Field(
        default_factory=datetime.now(datetime.utcnow), nullable=False
    )

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
    profile_id: Annotated[
        UUID,
        Field(
            foreign_key="profile.profile_id",
            nullable=False,
            title="profile id field",
            ondelete="CASCADE",
        ),
    ]
    tweet: "Tweet" = Relationship(back_populates="comments")
    content: Annotated[
        str, Field(..., title="comment content field", min_length=1, max_length=150)
    ]
    created_at: datetime = Field(
        default_factory=datetime.now(datetime.utcnow), nullable=False
    )

    # return title cased content.
    @field_validator("content", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()
