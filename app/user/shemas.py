from pydantic import BaseModel, EmailStr
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


class UserOut(UserBase):
    username: str
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


