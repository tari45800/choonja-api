
from sqlalchemy.orm import Session
from datetime import date, time
from app.models.schedule import Schedule
from app.models.action import Action
from app.utils.extract_date_parts import extract_date_parts
from app.utils.get_relative_day_label import get_relative_day_label
from app.utils.get_korean_category_label import get_korean_category_label


# 할 일 (task): 중복 X, 시간 없음
def create_task_schedule(db: Session, action: Action, date: date) -> str:
    return _base_schedule_logic(
        db, action, schedule_date=date,
        category="task"
    )

# 일정 (schedule): 중복 X, 시간 있음
def create_schedule_schedule(db: Session, action: Action, date: date, t: time) -> str:
    return _base_schedule_logic(
        db, action, schedule_date=date,
        schedule_time=t,
        include_time=True,
        category="schedule"
    )

# 기록 (record): 중복 O, 시간 있음
def create_record_schedule(db: Session, action: Action, date: date, t: time) -> str:
    return _base_schedule_logic(
        db, action, schedule_date=date,
        schedule_time=t,
        include_time=True,
        allow_duplicate=True,
        category="record"
    )


def _base_schedule_logic(
    db: Session,
    action: Action,
    schedule_date: date,
    schedule_time: time | None = None,
    allow_duplicate: bool = False,
    include_time: bool = False,
    category: str = "task"
) -> str:
    label = get_relative_day_label(schedule_date)
    if include_time and schedule_time:
        label += f" {schedule_time.strftime('%H:%M')}"

    korean_category = get_korean_category_label(category)
    parts = extract_date_parts(schedule_date)

    # 중복 검사 (조건적으로 시간 포함)
    if not allow_duplicate:
        filters = [
            Schedule.action_id == action.id,
            Schedule.year == str(schedule_date.year),
            Schedule.month == str(schedule_date.month),
            Schedule.day == str(schedule_date.day)
        ]
        if include_time and schedule_time:
            filters.append(Schedule.time == schedule_time)

        exists = db.query(Schedule).filter(*filters).first()
        if exists:
            return f"{label}에 '{action.name}' {korean_category}은 이미 등록되어 있어요."

    new_schedule = Schedule(
        action_id=action.id,
        year=parts["year"],
        month=parts["month"],
        day=parts["day"],
        time=schedule_time if include_time else None,
        until_date=None,
        is_checked=False,
        memo=None
    )
    db.add(new_schedule)
    db.commit()
    return f"{label}에 '{action.name}' {korean_category}이 등록됐어요."
