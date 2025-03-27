from sqlalchemy.orm import Session
from app.utils.schedule_parser import parse_schedule_text
from app.crud.action import get_or_create_action
from app.crud.schedule import create_task_schedule


def register_todo(db: Session, text: str):
    parsed = parse_schedule_text(text)
    category = 'task'
    schedule_date = parsed["date"]
    task_name = parsed["task"]

    # 액션 확인 및 등록
    action = get_or_create_action(db, task_name, category)

    # 할일 등록 (중복 방지, 시간 없음)
    schedule_status = create_task_schedule(db, action, schedule_date)

    return {
        "message" : schedule_status
    }