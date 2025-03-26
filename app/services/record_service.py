from sqlalchemy.orm import Session
from app.utils.record_parser import parse_record_text
from app.crud.action import get_or_create_action
from app.crud.schedule import create_record_schedule

def register_record(db: Session, text: str):
    parsed = parse_record_text(text)
    category = "record"
    record_date = parsed["date"]
    record_time = parsed["time"]
    task_name = parsed["task"]

    # 액션 등록
    action = get_or_create_action(db, task_name, category)

    # 기록 등록 (중복 허용, 체크 상태 True)
    message = create_record_schedule(db, action, record_date, record_time)

    return { "message": message }
