from sqlalchemy.orm import Session
from app.utils.parser.parse_action import parse_action
from app.crud.action import create_action
from app.crud.schedule import create_schedule
from app.utils.time import now_kst 

def create_record_service(text: str, db: Session):
    action_name = parse_action(text) or "기록 없음"

    action_res = create_action(name=action_name, category="record", db=db)
    action = action_res["result"] if action_res and action_res["result"] else None

    now = now_kst()

    return create_schedule(
        db=db,
        action_id=action.id,
        year=now.year,
        month=str(now.month),
        day=str(now.day),
        time=now.time()
    )
