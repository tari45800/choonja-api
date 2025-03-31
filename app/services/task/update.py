from sqlalchemy.orm import Session
from datetime import datetime
from app.crud.action import find_action
from app.crud.schedule import find_schedule, update_schedule
from app.utils.parser.extract_parts import extract_parts

def update_task_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  # 에러 메시지 그대로 리턴

    dt = parsed['dt']
    an = parsed['action']

    # 3. 액션 조회
    action_check = find_action(an, db)
    if not action_check["result"]:
        return action_check  # 메시지 포함 그대로 리턴

    action = action_check["result"]

    # 4. 오늘 날짜로 액션에 해당하는 스케줄이 이미 등록되어 있는지 확인
    today = datetime.now()
    schedule_check = find_schedule(
        action_id=action.id, 
        year=today.year,
        month=str(today.month),
        day=str(today.day),
        db=db
    )

    # 스케줄이 없다면 "스케줄이 없습니다" 리턴
    if not schedule_check['result']:
        return schedule_check  


    # 5. 오늘 스케줄이 있으면, 파싱된 날짜로 수정
    updated_schedule = update_schedule(
        current_schedule=schedule_check['result'],  # 이미 찾아낸 스케줄
        new_year=dt.year,  # 파싱된 날짜의 연도
        new_month=str(dt.month),  # 파싱된 날짜의 월
        new_day=str(dt.day),  # 파싱된 날짜의 일
        db=db
    )

    return updated_schedule
