from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ThreadBase(BaseModel):
    class Config:
        from_attributes = True


class ThreadCreate(ThreadBase):
    name: str
    text: str







