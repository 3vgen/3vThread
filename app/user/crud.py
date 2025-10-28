from typing import Any, Sequence
from fastapi import Depends
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.future import select
from app.user.model import User
from fastapi.security import OAuth2PasswordBearer
from app.user.jwt_auth import decode_token
from app.db.connection import get_db


async def create_user(db: AsyncSession, name: str, email: str) -> User:
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_all_users(db: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
    result = await db.execute(select(User))
    return result.scalars().all()




