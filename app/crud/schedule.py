from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.schedule import Schedule
from app.models.action import Action
from app.utils.formator.format_datetime import format_datetime
from sqlalchemy import desc

# 특정 스케줄 찾기
def find_schedule(action_id: int, year: int, month: str, day: str, db: Session):
    dt = datetime(year, int(month), int(day))  # 먼저 날짜 객체 생성
    schedule = db.query(Schedule).filter(
        Schedule.action_id == action_id,
        Schedule.year == year,
        Schedule.month.like(f"%{month}%"),
        Schedule.day.like(f"%{day}%")
    ).first()
    
    if schedule:
        return {
            "result": schedule,
            "message": f" 할 일이 {format_datetime(dt)}에 이미 등록되어 있습니다."
        }
    else:
        return {
            "result": None,
            "message": f" 할 일은 {format_datetime(dt)}에 등록되어 있지 않습니다."
        }

# 스케줄 등록
def create_schedule(
    action_id: int,
    year: int,
    month: str,
    day: str,
    db: Session,
    time=None,
    day_of_week=None,
    until_date=None,
    memo=None,
    briefing=None,
    is_alarm_enabled=False,
    is_voice_enabled=False,
    is_push_enabled=False
):
    # 액션 이름 가져오기
    action = db.query(Action).filter(Action.id == action_id).first()
    action_name = action.name if action else "이름 없는"

    schedule = Schedule(
        action_id=action_id,
        year=year,
        month=month,
        day=day,
        day_of_week=day_of_week,
        time=time,
        until_date=until_date,
        memo=memo,
        briefing=briefing,
        is_alarm_enabled=is_alarm_enabled,
        is_voice_enabled=is_voice_enabled,
        is_push_enabled=is_push_enabled,
        created_at=datetime.now(timezone.utc)
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    # 포맷팅된 날짜
    formatted_date = format_datetime(datetime(year, int(month), int(day)))  # 날짜 포맷

    return {
        "result": schedule,
        "message": f"'{action_name}' 할 일이 {formatted_date}에 새로 등록되었습니다."
    }

# 스케줄 수정
def update_schedule(
    current_schedule,  # 외부에서 이미 찾은 스케줄 객체
    new_year: int,
    new_month: str,
    new_day: str,
    db: Session,
    new_time=None  # 시간도 변경할 수 있도록
):
    # 1. 같은 날짜에 이미 같은 액션이 있는지 확인
    duplicate = find_schedule(
        action_id=current_schedule.action.id,  # 외부에서 받은 current_schedule의 action_id
        year=new_year,
        month=str(new_month),
        day=str(new_day),
        db=db
    )

    if duplicate['result']:  # 이미 같은 날짜에 등록된 스케줄이 있으면 반환
        return duplicate

    # 2. 날짜 및 시간 수정
    before_dt = datetime(current_schedule.year, int(current_schedule.month), int(current_schedule.day))
    after_dt = datetime(new_year, int(new_month), int(new_day))
    if new_time:
        after_dt = after_dt.replace(hour=new_time.hour, minute=new_time.minute)

    # 날짜 업데이트
    current_schedule.year = new_year
    current_schedule.month = new_month
    current_schedule.day = new_day
    current_schedule.time = new_time
    current_schedule.created_at = datetime.now(timezone.utc)

    # DB에 반영
    db.commit()
    db.refresh(current_schedule)

    # 포맷팅된 날짜들
    formatted_before = format_datetime(before_dt)
    formatted_after = format_datetime(after_dt)

    return {
        "result": current_schedule,
        "message": f"스케줄이 {formatted_before}에서 {formatted_after}으로 변경되었습니다."
    }

# 마지막 일정 가져오기
def get_latest_schedule(db: Session, action_id: int = None):
    query = db.query(Schedule)
    action_name = None

    if action_id:
        query = query.filter(Schedule.action_id == action_id)
        action = db.query(Action).filter(Action.id == action_id).first()
        action_name = action.name if action else None

    latest = query.order_by(desc(Schedule.created_at)).first()

    if latest:
        msg = (
            f"가장 최근 등록된 '{action_name}' 일정은 {latest.year}-{latest.month}-{latest.day} 입니다."
            if action_name else
            f"가장 최근 일정은 {latest.year}-{latest.month}-{latest.day} 입니다."
        )
    else:
        msg = (
            f"'{action_name}' 일정은 등록되어 있지 않습니다."
            if action_name else
            "최근 일정이 없습니다."
        )

    return {
        "result": latest,
        "message": msg
    }

# 스케줄 삭제
def delete_schedule(schedule: Schedule, db: Session, action_name: str = None):
    db.delete(schedule)
    db.commit()

    message = f"'{action_name}' 일정이 삭제되었습니다." if action_name else "일정이 삭제되었습니다."
    
    return {
        "result": schedule,
        "message": message
    }

