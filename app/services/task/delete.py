from sqlalchemy.orm import Session
from app.crud.schedule import get_latest_schedule, delete_schedule
from app.crud.action import find_action
from app.utils.parser.extract_parts import extract_parts

def delete_latest_task_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed

    an = parsed['action']

    action_check = find_action(an, db)
    if not action_check["result"]:
        return action_check

    action = action_check["result"]

    latest_check = get_latest_schedule(db, action_id=action.id)
    if not latest_check["result"]:
        return latest_check

    latest = latest_check["result"]

    return delete_schedule(latest, db, action_name=an)
