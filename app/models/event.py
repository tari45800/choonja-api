from sqlalchemy import Column, String, Enum, ForeignKey
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, index=True)
    action_id = Column(String(36), ForeignKey("actions.id"))
    trigger_type = Column(Enum("cry", "home_leave", "off_work", name="trigger_type"))
