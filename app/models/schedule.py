from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"), nullable=False)
    year = Column(Integer)
    month = Column(String(50))
    day_of_month = Column(String(50))
    day_of_week = Column(String(50))
    time = Column(Time)
    until_date = Column(Date)
    completed_at = Column(DateTime)
    is_checked = Column(Boolean, default=False)
    memo = Column(String)
    briefing = Column(String(255))
    is_alarm_enabled = Column(Boolean, default=False)
    is_voice_enabled = Column(Boolean, default=False)
    is_push_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    action = relationship("Action")
