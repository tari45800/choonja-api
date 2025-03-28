from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.utils.parser.split_time import split_time
from app.utils.parser.parse_time import parse_time
from app.utils.parser.parse_action import parse_action
from app.crud.action import create_action, find_action
from app.crud.schedule import find_schedule, update_schedule

def update_task_service(text: str, db: Session):
    # 1. 시간/행동 분리
    time_part, action_part = split_time(text)

    # 2. 파싱
    dt = parse_time(time_part) if time_part else None
    an = parse_action(action_part) if action_part else None

    # 3. 액션 조회
    action = find_action(an, db)

    # 액션이 없으면 오류 메시지 반환
    if not action:
        return {
            "result": None,
            "message": f"'{an}' 액션을 찾을 수 없습니다."
        }

    # 4. 오늘 날짜로 액션에 해당하는 스케줄이 이미 등록되어 있는지 확인
    today = datetime.now()
    schedule_check = find_schedule(
        action_id=action.id,  # 파싱한 액션 ID
        year=today.year,
        month=str(today.month),
        day=str(today.day),
        db=db
    )

    # 스케줄이 없다면 "스케줄이 없습니다" 리턴
    if not schedule_check['result']:
        return {
            "result": None,
            "message": f"{today.strftime('%Y-%m-%d')}에 '{an}' 할 일이 등록되어 있지 않습니다."
        }

    # 5. 오늘 스케줄이 있으면, 파싱된 날짜로 수정
    updated_schedule = update_schedule(
        current_schedule=schedule_check['result'],  # 이미 찾아낸 스케줄
        new_year=dt.year,  # 파싱된 날짜의 연도
        new_month=str(dt.month),  # 파싱된 날짜의 월
        new_day=str(dt.day),  # 파싱된 날짜의 일
        db=db
    )

    return updated_schedule
