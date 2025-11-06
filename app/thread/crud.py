from typing import Any, Sequence
from fastapi import Depends
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.future import select
from app.thread.model import Thread
from fastapi.security import OAuth2PasswordBearer
from app.user.jwt_auth import decode_token
from app.db.connection import get_db


async def create_thread(db: AsyncSession, name: str, email: str) -> Thread:
    thread = Thread(name=name, email=email)
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread
