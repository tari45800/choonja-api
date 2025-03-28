from typing import Optional
from pydantic import BaseModel
from app.schemas.schedule import ScheduleOut

class TaskText(BaseModel):
    text: str

class TaskResponse(BaseModel):
    result: Optional[ScheduleOut]
    message: str
