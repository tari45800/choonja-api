from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime, func
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action_id = Column(Integer, ForeignKey("actions.id"))  # ✅ Integer로 수정
    trigger_type = Column(Enum("cry", "home_leave", "off_work"))
    created_at = Column(DateTime, default=func.now())
