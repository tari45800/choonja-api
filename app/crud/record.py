from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import Action, Schedule
from typing import List, Dict
from typing import Optional
from app.utils.get_avg import to_schedule_datetime

# 기록 갯수 가져오기
def count_records(
    db: Session,
    action_name: str,
    start: datetime = None,
    end: datetime = None
) -> int:
    # 1. 액션 찾기
    action = db.query(Action).filter(Action.name == action_name).first()
    if not action:
        return 0

    # 2. 기본 쿼리
    query = db.query(func.count(Schedule.id)).filter(Schedule.action_id == action.id)

    # 3. 날짜 범위 필터 (옵션)
    if start:
        query = query.filter(Schedule.created_at >= start)
    if end:
        query = query.filter(Schedule.created_at <= end)

    return query.scalar()

# 액션 이름으로 기록 날짜 가져오기
def get_records_grouped_by_action(
    db: Session,
    action_names: List[str],
    start: datetime,
    end: datetime
) -> Dict[str, List[Schedule]]:
    result: Dict[str, List[Schedule]] = {}

    for name in action_names:
        action = db.query(Action).filter(Action.name == name).first()
        if not action:
            result[name] = []
            continue

        # 먼저 다 가져온 다음, 스케줄 기준 날짜로 필터링
        schedules = db.query(Schedule).filter(Schedule.action_id == action.id).all()

        filtered = [
            s for s in schedules
            if start <= to_schedule_datetime(s) <= end
        ]

        # 다시 시간 기준 정렬
        sorted_filtered = sorted(filtered, key=to_schedule_datetime)
        result[name] = sorted_filtered

    return result

# 가장 최근의 특정 기록 가져오기
def get_latest_record_by_action_name(action_name: str, db: Session) -> Optional[Schedule]:
    action = db.query(Action).filter(Action.name == action_name).first()
    if not action:
        return None

    schedules = db.query(Schedule).filter(Schedule.action_id == action.id).all()
    if not schedules:
        return None

    sorted_schedules = sorted(schedules, key=to_schedule_datetime, reverse=True)
    return sorted_schedules[0]