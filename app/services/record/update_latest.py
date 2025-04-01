from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.parser.extract_parts import extract_parts
from app.crud.schedule import get_latest_schedule, update_record
from app.crud.action import find_action, create_action 

def update_latest_record_service(text: str, db: Session):
    parsed = extract_parts(text)
    print(f"🔍 파싱된 입력: {parsed}")  # ✅ 파싱 결과 확인

    if 'result' in parsed:
        return parsed

    dt = parsed['dt']
    an = parsed['action']

    latest_check = get_latest_schedule(db)
    if not latest_check["result"]:
        print("❌ 최근 스케줄 없음")
        return latest_check

    latest = latest_check["result"]
    print(f"📦 최근 스케줄: {latest.id} | action_id: {latest.action_id} | 날짜: {latest.year}-{latest.month}-{latest.day} {latest.time}")  # ✅ 최근 기록 확인

    if an:
        action_check = find_action(an, db)
        if not action_check["result"]:
            print(f"🆕 액션 생성: '{an}'")
            created = create_action(name=an, category="record", db=db)
            action = created["result"]
        else:
            print(f"✅ 기존 액션 사용: '{an}'")
            action = action_check["result"]

        latest.action_id = action.id

    updated_record = update_record(
        current_schedule=latest,
        new_year=dt.year if dt else latest.year,
        new_month=str(dt.month) if dt else latest.month,
        new_day=str(dt.day) if dt else latest.day,
        new_time=dt.time() if dt and (dt.hour + dt.minute + dt.second) > 0 else None,
        db=db
    )

    print(f"🛠 최종 업데이트 완료: {updated_record}")  # ✅ 최종 업데이트 결과 확인

    return updated_record
