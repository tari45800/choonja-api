from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database import Base

KST = timezone(timedelta(hours=9))
def now_kst():
    return datetime.now(KST)

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"), nullable=False)
    year = Column(Integer)
    month = Column(String(50))
    day = Column(String(50))
    day_of_week = Column(String(50), nullable=True)
    time = Column(Time, nullable=True)
    until_date = Column(Date, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    is_checked = Column(Boolean, default=False)
    memo = Column(String(1000), nullable=True) 
    briefing = Column(String(255), nullable=True)
    is_alarm_enabled = Column(Boolean, default=False)
    is_voice_enabled = Column(Boolean, default=False)
    is_push_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=now_kst)

    action = relationship("Action")
