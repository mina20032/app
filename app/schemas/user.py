from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    SERVANT = "SERVANT"


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRoleEnum


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRoleEnum


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    role: Optional[UserRoleEnum] = None
    exp: Optional[int] = None

