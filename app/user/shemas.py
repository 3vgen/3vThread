from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


class UserLogin(UserBase):
    email: EmailStr
    password: str


class UserProfileOut(BaseModel):
    username: Optional[str]


class UserOut(UserBase):
    email: str
    is_active: bool
    created_at: datetime
    profile: Optional[UserProfileOut]

    class Config:
        from_attributes = True


