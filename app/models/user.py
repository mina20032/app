import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    SERVANT = "SERVANT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.SERVANT)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

