import os

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.user.shemas import UserCreate, UserOut, UserLogin
from app.user.crud import create_user, get_all_users
from app.user.model import AuthUser, User
from app.user.auth_util import hash_password, verify_password
from app.user.jwt_auth import create_access_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload["sub"]
    result = await db.execute(
        select(AuthUser).options(selectinload(AuthUser.profile)).where(AuthUser.email == email)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(AuthUser).where(AuthUser.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = AuthUser(email=user.email,
                        hashed_password=hash_password(user.password)
                        )
    db.add(new_user)

    await db.flush()

    profile = User(user_id=new_user.id, username=user.username)

    db.add(profile)
    await db.commit()
    await db.refresh(new_user)

    return {"msg": "User registered successfully", "email": new_user.email}


@router.post("/login")
# async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(AuthUser).where(AuthUser.email == user.email))
#     db_user = result.scalar_one_or_none()
#
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#
#     token = create_access_token({"sub": db_user.email})
#     return {"access_token": token, "token_type": "bearer"}
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # form_data.username — это email
    result = await db.execute(select(AuthUser).where(AuthUser.email == form_data.username))
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_me(current_user: AuthUser = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "username": current_user.profile.username if current_user.profile else None,
    }
