from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import field_validator
from datetime import datetime
from .profile_table import Profile


class Follow(SQLModel, table=True):
    follower_id: int = Field(foreign_key="profile.id", primary_key=True)
    followed_id: int = Field(foreign_key="profile.id", primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    # Relationships (back_populates)
    follower: "Profile" = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "Follow.follower_id"},
    )
    followed: "Profile" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "Follow.followed_id"},
    )
