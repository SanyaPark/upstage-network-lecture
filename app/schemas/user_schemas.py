from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True