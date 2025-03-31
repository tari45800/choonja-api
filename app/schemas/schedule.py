from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time, date

class ScheduleOut(BaseModel):
    id: int
    action_id: int
    year: int
    month: str
    day: str
    day_of_week: Optional[str]
    time: Optional[time]
    until_date: Optional[date]
    completed_at: Optional[datetime]
    is_checked: bool
    memo: Optional[str]
    briefing: Optional[str]
    is_alarm_enabled: bool
    is_voice_enabled: bool
    is_push_enabled: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
