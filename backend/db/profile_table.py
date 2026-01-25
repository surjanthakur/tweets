from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List
from pydantic import field_validator
import uuid
from uuid import UUID
from datetime import datetime
from tweet_table import Tweet


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
    username: Annotated[
        str,
        Field(
            foreign_key="user.username",
            nullable=False,
            title="username field @username",
            ondelete="CASCADE",
            unique=True,
        ),
    ]
    handle_name: Annotated[
        str,
        Field(
            ...,
            title="handle name field",
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
    created_at: datetime = Field(
        default_factory=datetime.now(datetime.utcnow), nullable=False
    )

    # return title cased profession and bio.
    @field_validator("profession", "bio", mode="after")
    @classmethod
    def validate_content(cla, value):
        return value.title()
