from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(Enum('task', 'fixed', 'log', 'routine'), nullable=False)
    parent_id = Column(Integer, ForeignKey("actions.id"), nullable=True)
    duration_min = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("Action", remote_side=[id])
