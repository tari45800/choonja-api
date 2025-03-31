from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.parser.extract_parts import extract_parts
from app.crud.schedule import get_latest_schedule, update_schedule
from app.crud.action import find_action, create_action

def update_latest_fixed_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  # ❌ 파싱 실패 시 메시지 리턴

    dt = parsed['dt']
    an = parsed['action']

    # 1. 가장 최근 스케줄 가져오기
    latest_check = get_latest_schedule(db)
    if not latest_check["result"]:
        return latest_check  # ❌ 최근 일정 없음 메시지 그대로 리턴

    latest = latest_check["result"]

    # 2. 액션이 들어왔으면 찾거나 생성
    if an:
        action_check = find_action(an, db)
        if not action_check["result"]:
            created = create_action(name=an, category="fixed", db=db)
            action = created["result"]
        else:
            action = action_check["result"]

        latest.action_id = action.id  # 액션 ID 업데이트

    # 3. 날짜 및 시간 업데이트
    updated_schedule = update_schedule(
        current_schedule=latest,
        new_year=dt.year if dt else latest.year,
        new_month=str(dt.month) if dt else latest.month,
        new_day=str(dt.day) if dt else latest.day,
        new_time=dt.time() if dt and (dt.hour + dt.minute + dt.second) > 0 else None,
        db=db
    )

    return updated_schedule
