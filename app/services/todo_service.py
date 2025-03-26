from app.crud.action import get_or_create_action
from app.utils.schedule_parser import parse_schedule_text
from sqlalchemy.orm import Session
from app.utils.schedule_parser import parse_schedule_text
from app.crud.action import get_or_create_action
from app.crud.schedule import check_or_create_schedule

def register_todo(db: Session, text: str):
    parsed = parse_schedule_text(text)
    schedule_date = parsed["date"] # 등록일
    task_name = parsed["task"] # 할 일 이름

    # 액션 확인, 등록 - 액션 객체 반환
    action = get_or_create_action(db, task_name)
    # 스케쥴 확인, 등록 - 메시지 반환
    message = check_or_create_schedule(db, action, schedule_date)

    return {
        "message" : message
    }
