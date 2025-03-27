from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.utils.schedule_parser import parse_schedule_text
from app.crud.action import get_or_create_action
from app.crud.schedule import create_schedule_schedule

def register_outing_schedule(db: Session, text: str):
    parsed = parse_schedule_text(text)
    category = "schedule"
    schedule_date = parsed["date"]
    schedule_time = parsed["time"]
    task_name = parsed["task"]
    duration = parsed.get("duration")  # 분 단위 소요시간 (명시된 값)

    # 액션 등록 or 가져오기
    action = get_or_create_action(db, task_name, category)

    # 만약 duration이 직접 안 들어왔으면 → 액션의 duration 사용
    if duration is None and action.duration_min:
        duration = action.duration_min

    # 시간 계산 (도착 시간 - 소요 시간 = 출발 시간)
    if schedule_time and duration:
        dt = datetime.combine(schedule_date, schedule_time)
        adjusted_time = (dt - timedelta(minutes=duration)).time()
    else:
        adjusted_time = schedule_time

    # 일정 등록 (출발 시간 기준)
    schedule_status = create_schedule_schedule(db, action, schedule_date, adjusted_time)

    # 스케줄 id 가져오기

    return {
        "message": schedule_status
    }
