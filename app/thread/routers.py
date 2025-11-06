import os

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.thread.shemas import ThreadCreate
from app.user.crud import create_user, get_all_users
from app.thread.model import Thread
from app.user.model import AuthUser
from app.user.auth_util import hash_password, verify_password
from app.user.jwt_auth import create_access_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm
from app.user.routers import get_current_user

router = APIRouter()


@router.post("/create")
async def create_thread_endpoint(thread: ThreadCreate, current_user: AuthUser = Depends(get_current_user),
                                 db: AsyncSession = Depends(get_db)):
    new_thread = Thread(user_id=current_user.id, name=thread.name, text=thread.text)
    db.add(new_thread)
    await db.commit()
    await db.refresh(new_thread)
    return {
        "name": thread.name,
        "username": current_user.profile.username,
        "text": new_thread.text,
        "created_at": new_thread.created_at,
    }
