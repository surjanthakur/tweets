from fastapi import APIRouter, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete, update
from sqlalchemy.orm import selectinload
from uuid import UUID
from db.db_tables import Comment
from uuid import UUID
from typing import List
from auth.auth_service import get_current_user


comment_router = APIRouter(prefix="/comments", tags=["comments"])


@comment_router.get("/{comment_id}")
def get_comment_by_id():
    pass
