from sqlalchemy import Column, String, Enum, Integer, Boolean, ForeignKey
from app.core.database import Base

class Action(Base):
    __tablename__ = "actions"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(Enum("task", "schedule", "log", name="action_category"), nullable=False)
    parent_id = Column(String(36), ForeignKey("actions.id"), nullable=True)
    duration_min = Column(Integer, nullable=True)
    briefing = Column(String(255), nullable=True)
    is_alarm_enabled = Column(Boolean, default=False)
    is_voice_enabled = Column(Boolean, default=False)
    is_push_enabled = Column(Boolean, default=False)