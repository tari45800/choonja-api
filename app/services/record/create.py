from sqlalchemy.orm import Session
from app.utils.parser.extract_parts import extract_parts  # 날짜+액션 파싱
from app.crud.action import create_action
from app.crud.schedule import create_schedule
from app.utils.time import now_kst
from app.services.record.handle_special_record import handle_special_record 

def create_record_service(text: str, db: Session):
    parsed = extract_parts(text)
    if "result" in parsed:
        return parsed  # 파싱 실패 시 메시지 그대로 반환

    dt = parsed["dt"] or now_kst()  # 날짜 없으면 현재 시간
    action_name = parsed["action"] or "기록 없음"

    # 액션 등록 or 조회
    action_res = create_action(name=action_name, category="record", db=db)
    action = action_res["result"] if action_res and action_res["result"] else None

    # 특수 로직 메시지
    extra_message = handle_special_record(action_name, db)

    # 스케줄 등록
    schedule_res = create_schedule(
        db=db,
        action_id=action.id,
        year=dt.year,
        month=str(dt.month),
        day=str(dt.day),
        time=dt.time()
    )

    # 메시지 병합
    final_message = schedule_res["message"]
    if extra_message:
        final_message += f" {extra_message}"

    return {
        "result": schedule_res["result"],
        "message": final_message
    }
