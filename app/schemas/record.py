from typing import Optional
from pydantic import BaseModel
from app.schemas.schedule import ScheduleOut

class RecordText(BaseModel):
    text: str

class RecordResponse(BaseModel):
    result: Optional[ScheduleOut]
    message: str
