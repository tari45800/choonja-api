from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.parser.split_time import split_time
from app.utils.parser.parse_time import parse_time
from app.utils.parser.parse_action import parse_action
from app.utils.formator.format_datetime import format_datetime
from app.crud.action import create_action
from app.crud.schedule import find_schedule, create_schedule
from app.utils.parser.extract_parts import extract_parts

def create_task_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed

    dt = parsed['dt']
    an = parsed['action']

    # 2. 액션 등록 or 조회
    action_res = create_action(name=an, category="task", db=db)
    action = action_res["result"] if action_res and action_res["result"] else None

    # 3. 중복 확인
    if dt:
        already = find_schedule(
            action_id=action.id,
            year=dt.year,
            month=str(dt.month),
            day=str(dt.day),
            db=db
        )
        
        if already['result']:  # 이미 등록된 일정이 있으면 반환
            return already

    # 4. 스케줄 등록
    target = dt or datetime.now()
    schedule_res = create_schedule(
        action_id=action.id,
        year=target.year,
        month=str(target.month),
        day=str(target.day),
        db=db,
        time=target if dt else None  # dt가 있으면 시간을 설정, 없으면 None
    )

    return schedule_res
