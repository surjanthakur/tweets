from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid


class User_validation(BaseModel):
    username: str = Field(..., min_length=3, max_length=40)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=3, max_length=40)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class RefreshToken(BaseModel):
    id: uuid.UUID
    user_id: str
    validity_timestamp: float
