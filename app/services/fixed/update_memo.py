# app/services/fixed/update_memo.py

from sqlalchemy.orm import Session
from app.crud.schedule import update_schedule_memo, find_schedule_by_id

def update_fixed_memo_service(schedule_id: int, memo: str, db: Session):
    schedule_check = find_schedule_by_id(schedule_id, db)
    if not schedule_check["result"]:
        return schedule_check 

    schedule = schedule_check["result"]
    return update_schedule_memo(schedule, memo, db) 
