import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Stage(str, enum.Enum):
    PRIMARY = "PRIMARY"
    PREP = "PREP"
    SECONDARY = "SECONDARY"


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    stage = Column(Enum(Stage), nullable=False)
    grade = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    father_phone = Column(String(50), nullable=True)
    mother_phone = Column(String(50), nullable=True)
    confession_number = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    school = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    banned = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    attendances = relationship("Attendance", back_populates="child", cascade="all, delete-orphan")
    visits = relationship("Visit", back_populates="child", cascade="all, delete-orphan")
    points = relationship("Points", back_populates="child", cascade="all, delete-orphan")

