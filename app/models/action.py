from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.time import now_kst 

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(Enum('task', 'fixed', 'log', 'routine', 'd_day', 'record'), nullable=False)
    parent_id = Column(Integer, ForeignKey("actions.id"), nullable=True)
    duration_min = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=now_kst) 

    parent = relationship("Action", remote_side=[id])
