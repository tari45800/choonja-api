from sqlalchemy.orm import Session
from datetime import date
from app.models.schedule import Schedule
from app.models.action import Action
from app.utils.extract_date_parts import extract_date_parts
from app.utils.get_relative_day_label import get_relative_day_label  # ✅ 이거 추가

def check_or_create_schedule(db: Session, action: Action, schedule_date: date) -> str:
    label = get_relative_day_label(schedule_date)

    exists = db.query(Schedule).filter(
        Schedule.action_id == action.id,
        Schedule.year == str(schedule_date.year),
        Schedule.month == str(schedule_date.month),
        Schedule.day == str(schedule_date.day)
    ).first()

    if exists:
        return f"{label}에 '{action.name}' 할일은 이미 등록되어 있어요."

    parts = extract_date_parts(schedule_date)

    new_schedule = Schedule(
        action_id=action.id,
        year=parts["year"],
        month=parts["month"],
        day=parts["day"],
        until_date=None,
        is_checked=False,
        memo=None
    )
    db.add(new_schedule)
    db.commit()
    return f"{label}에 '{action.name}' 할일이 등록됐어요."
