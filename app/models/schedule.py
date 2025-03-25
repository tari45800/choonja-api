from sqlalchemy import Column, Integer, Time, String, Date, DateTime, Boolean, ForeignKey
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"))
    time = Column(Time, nullable=True)
    week = Column(String(50), nullable=True)
    day = Column(String(50), nullable=True)
    month = Column(String(50), nullable=True)
    year = Column(String(50), nullable=True)
    until_date = Column(Date, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    is_checked = Column(Boolean, default=False)
    memo = Column(String(255), nullable=True)
