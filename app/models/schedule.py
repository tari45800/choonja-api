from sqlalchemy import Column, String, Time, Date, DateTime, Boolean, ForeignKey
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String(36), primary_key=True, index=True)
    action_id = Column(String(36), ForeignKey("actions.id"))
    time = Column(Time, nullable=True)
    day_of_week = Column(String(20), nullable=True)
    day_of_month = Column(String(20), nullable=True)
    month = Column(String(20), nullable=True)
    until_date = Column(Date, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    is_checked = Column(Boolean, default=False)
    memo = Column(String(1000)) 
