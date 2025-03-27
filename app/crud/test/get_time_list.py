from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.schedule import Schedule
from app.models.action import Action
from datetime import datetime, timedelta, time

def get_time_list(db: Session, action_name: str) -> list[datetime]:
    seven_days_ago = datetime.now().date() - timedelta(days=7)

    rows = (
        db.query(
            Schedule.year,
            Schedule.month,
            Schedule.day,
            Schedule.time
        )
        .join(Action, Schedule.action_id == Action.id)
        .filter(
            Action.name == action_name,
            func.date(
                func.concat_ws("-", Schedule.year, Schedule.month, Schedule.day)
            ) >= seven_days_ago
        )
        .order_by(Schedule.year, Schedule.month, Schedule.day, Schedule.time)
        .all()
    )

    time_list = []
    for year, month, day, t in rows:
        if t:
            dt = datetime(year=int(year), month=int(month), day=int(day),
                          hour=t.hour, minute=t.minute, second=t.second)
            time_list.append(dt)

    return time_list
