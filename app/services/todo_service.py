from app.utils.todo_parser import custom_date_parser
from app.crud.action import get_or_create_action
from app.crud.schedule import create_schedule

def handle_parsed_todo(db, raw_text: str):
    date, task = custom_date_parser(raw_text)
    action_id = get_or_create_action(db, task)
    schedule = create_schedule(db, action_id, date)
    return {"message": "등록 완료", "date": str(date), "name": task}
