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
    is_checked: Optional[bool] = False
    is_alarm_enabled: Optional[bool] = False
    is_voice_enabled: Optional[bool] = False
    is_push_enabled: Optional[bool] = False
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
