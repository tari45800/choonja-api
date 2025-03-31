# app/schemas/d_day.py

from typing import List, Optional
from pydantic import BaseModel
from app.schemas.schedule import ScheduleOut

class DDayText(BaseModel):
    text: str
    include_after: Optional[bool] = False  # ➕ 이후 일정 포함 여부 옵션

class DDayResponse(BaseModel):
    result: Optional[ScheduleOut]  # 기준 디데이 일정 하나만
    message: str
