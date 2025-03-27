from sqlalchemy.orm import Session
from app.utils.schedule_parser import parse_schedule_text
from app.crud.action import get_or_create_action
from app.crud.schedule import create_schedule_schedule


def register_schedule(db: Session, text: str):
    parsed = parse_schedule_text(text)
    category = 'schedule'
    schedule_date = parsed["date"]
    schedule_time = parsed["time"]
    task_name = parsed["task"]

    # 액션 확인 및 등록
    action = get_or_create_action(db, task_name, category)

    # 일정 등록 (중복 방지, 시간 포함)
    schedule_status = create_schedule_schedule(db, action, schedule_date, schedule_time)

    return {
        "message" : schedule_status
    }