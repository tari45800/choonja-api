from sqlalchemy.orm import Session
from app.crud.schedule import get_latest_schedule, delete_schedule
from app.crud.action import find_action
from app.utils.parser.extract_parts import extract_parts

def delete_latest_fixed_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  # ❌ 파싱 실패 그대로 리턴

    an = parsed['action']

    # 1. 액션 찾기
    action_check = find_action(an, db)
    if not action_check["result"]:
        return action_check  # ❌ 메시지 포함된 dict 그대로 리턴

    action = action_check["result"]

    # 2. 해당 액션의 최신 스케줄 가져오기
    latest_check = get_latest_schedule(db, action_id=action.id)
    if not latest_check["result"]:
        return latest_check  # ❌ 메시지 그대로

    latest = latest_check["result"]

    # 3. 삭제 (액션 이름도 함께 넘김)
    return delete_schedule(latest, db, action_name=an)
