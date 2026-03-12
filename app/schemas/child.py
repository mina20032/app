from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StageEnum(str, Enum):
    PRIMARY = "PRIMARY"
    PREP = "PREP"
    SECONDARY = "SECONDARY"


class ChildBase(BaseModel):
    name: str
    age: Optional[int] = None
    stage: StageEnum
    grade: Optional[str] = None
    phone: Optional[str] = None
    father_phone: Optional[str] = None
    mother_phone: Optional[str] = None
    confession_number: Optional[str] = None
    address: Optional[str] = None
    school: Optional[str] = None
    notes: Optional[str] = None
    banned: bool = False


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    stage: Optional[StageEnum] = None
    grade: Optional[str] = None
    phone: Optional[str] = None
    father_phone: Optional[str] = None
    mother_phone: Optional[str] = None
    confession_number: Optional[str] = None
    address: Optional[str] = None
    school: Optional[str] = None
    notes: Optional[str] = None
    banned: Optional[bool] = None


class ChildRead(ChildBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

