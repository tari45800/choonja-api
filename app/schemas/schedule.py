from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class ScheduleOut(BaseModel):
    id: int
    action_id: int
    year: int
    month: str
    day: str
    day_of_week: Optional[str]
    time: Optional[time]
    memo: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
