from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum("task", "schedule", "record", "routine"), nullable=False)
    parent_id = Column(Integer, ForeignKey("actions.id"), nullable=True)
    duration_min = Column(Integer)
    briefing_key = Column(String(100))
    is_alarm_enabled = Column(Boolean)
    is_voice_enabled = Column(Boolean)
    is_push_enabled = Column(Boolean)

    children = relationship("Action", remote_side=[id])
