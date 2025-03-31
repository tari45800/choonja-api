from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.parser.extract_parts import extract_parts
from app.crud.action import find_action
from app.crud.schedule import find_schedule, update_schedule

def update_fixed_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  

    dt = parsed['dt']
    an = parsed['action']

    # 1. 액션 조회
    action_check = find_action(an, db)
    if not action_check["result"]:
        return action_check 

    action = action_check["result"]

    # 2. 오늘 날짜로 등록된 스케줄 찾기
    today = datetime.now()
    schedule_check = find_schedule(
        action_id=action.id,
        year=today.year,
        month=str(today.month),
        day=str(today.day),
        db=db
    )

    if not schedule_check["result"]:
        return schedule_check 

    schedule = schedule_check["result"]

    # 3. 시간까지 포함해서 업데이트
    updated_schedule = update_schedule(
        current_schedule=schedule,
        new_year=dt.year,
        new_month=str(dt.month),
        new_day=str(dt.day),
        new_time=dt.time() if dt and (dt.hour + dt.minute + dt.second) > 0 else None,
        db=db
    )

    return updated_schedule
