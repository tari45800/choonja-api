from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.todo import TodoText
from app.utils.todo_parser import custom_date_parser
from app.core.database import get_db
from app.crud.action import get_or_create_action
from app.crud.schedule import check_or_create_schedule

router = APIRouter()


@router.post("/api/todo")
@router.post("/api/todo")
def parse_and_register_todo(item: TodoText, db: Session = Depends(get_db)):
    schedule_date, task_name = custom_date_parser(item.text)

    action = get_or_create_action(db, task_name)

    schedule_status = check_or_create_schedule(db, action, schedule_date)

    return {
        "date": str(schedule_date),
        "action_id": action.id,
        "task": action.name,
        "schedule_status": schedule_status
    }
