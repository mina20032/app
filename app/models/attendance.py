import enum
from datetime import date

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class AttendanceType(str, enum.Enum):
    SERVICE = "SERVICE"
    MASS = "MASS"
    TASBEHA = "TASBEHA"
    ASHEYA = "ASHEYA"
    CLUB = "CLUB"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False, index=True)
    servant_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(Enum(AttendanceType), nullable=False)
    date = Column(Date, default=date.today, nullable=False, index=True)

    child = relationship("Child", back_populates="attendances")
    servant = relationship("User")

