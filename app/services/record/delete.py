from sqlalchemy.orm import Session
from app.crud.schedule import get_latest_schedule, delete_schedule
from app.crud.action import find_action
from app.utils.parser.extract_parts import extract_parts

def delete_latest_record_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  # ❌ 파싱 실패 그대로 리턴

    an = parsed['action']

    # 1. 액션 찾기
    action_check = find_action(an, db)
    if not action_check["result"]:
        return action_check  # ❌ 액션 없음

    action = action_check["result"]

    # 2. 해당 액션의 최신 기록 가져오기 (created_at 기준)
    latest_check = get_latest_schedule(db, action_id=action.id)
    if not latest_check["result"]:
        return latest_check  # ❌ 최근 기록 없음

    latest = latest_check["result"]

    # 3. 삭제
    return delete_schedule(latest, db, action_name=an)
