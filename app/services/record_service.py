from sqlalchemy.orm import Session
from app.utils.record_parser import parse_record_text
from app.crud.action import get_or_create_action
from app.crud.schedule import create_record_schedule
from app.crud.get_stock_count import get_stock_count

def register_record(db: Session, text: str):
    parsed = parse_record_text(text)
    task_name = parsed["task"]
    record_date = parsed["date"]
    record_time = parsed["time"]
    stock_message =''

    # ✅ 분기만 처리 (카테고리는 무조건 "record")
    if "기저귀" in task_name and "구매" in task_name:
        print("기저귀 구매")
        stock_message = f"기저귀가 총 {stock}개 있습니다."
        pass
    elif "기저귀" in task_name and "교체" in task_name:
        stock = get_stock_count(
            db,
            keyword_purchase="기저귀 구매",
            keyword_use="기저귀 교체",
            unit_per_purchase=10
        )
        if stock <= 4:
          stock_message = f"기저귀가 {stock}개 남았습니다. 구매를 고려하세요!"
        pass
    elif "수면" in task_name and "끝" in task_name:
        # TODO: 수면 종료 처리
        pass
    elif "수면" in task_name and "시작" in task_name:
        # TODO: 수면 시작 처리
        pass
    elif "수유" in task_name:
        # TODO: 수유 시작 처리
        pass

    # 액션 등록 (카테고리는 "record"로 고정)
    category = "record"
    action = get_or_create_action(db, task_name, category)

    # 기록 등록 (중복 허용 + 완료 체크 상태)
    message = create_record_schedule(db, action, record_date, record_time)

    return {
              "message": message, 
              "stock_message":stock_message
            }
