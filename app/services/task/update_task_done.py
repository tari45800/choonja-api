from sqlalchemy.orm import Session
from datetime import datetime
from app.crud.action import find_action
from app.crud.schedule import find_schedule
from app.utils.parser.extract_parts import extract_parts
from app.utils.time import now_kst

def update_schedule_done_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  # 에러 메시지 그대로 리턴

    dt = parsed['dt']
    an = parsed['action']

    # 1. 액션 조회
    action_check = find_action(an, db)
    if not action_check["result"]:
        return action_check  # 메시지 포함 그대로 리턴

    action = action_check["result"]

    # 2. 오늘 날짜 기준으로 스케줄 확인
    today = datetime.now()
    schedule_check = find_schedule(
        action_id=action.id, 
        year=today.year,
        month=str(today.month),
        day=str(today.day),
        db=db
    )

    if not schedule_check['result']:
        return schedule_check  # 스케줄 없으면 그 메시지 리턴

    # 3. 완료 처리 업데이트
    schedule = schedule_check['result']
    schedule.completed_at = now_kst()
    schedule.is_checked = True

    db.commit()
    db.refresh(schedule)

    return {
        "result": schedule,
        "message": f"{an} 할 일을 완료로 처리했어요."
    }
