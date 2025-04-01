from app.crud.record import count_records
from sqlalchemy.orm import Session

def handle_special_record(action_name: str, db: Session) -> str:
    # 기본 메시지 세팅
    message = ""

    # 기저귀 교체 로직
    if action_name == "기저귀 교체":
        use_count = count_records(db, "기저귀 교체")
        buy_count = count_records(db, "기저귀 구매")

        stock = (buy_count * 10) - use_count

        if stock <= 6:
            message += f"현재 남은 재고는 약 {stock}개입니다. 기저귀 구매를 추천드려요"

        return message

    # 나머지 케이스
    elif action_name == "기저귀 구매":
        buy_count = count_records(db, "기저귀 구매")
        use_count = count_records(db, "기저귀 교체")
        stock = (buy_count * 10) - use_count

        return f"현재 남은 재고는 약 {stock}개입니다."

    elif action_name == "애기 수면 시작":
        count = count_records(db, "애기 수면 시작")
        return f"수면 시작 기록됨. 총 {count}회 시작됨."

    elif action_name == "애기 수면 종료":
        count = count_records(db, "애기 수면 종료")
        return f"수면 종료 기록됨. 총 {count}회 종료됨."

    elif action_name == "수유":
        count = count_records(db, "수유")
        return f"수유 시작 기록됨. 총 {count}회 수유 기록됨."

    else:
        return ""
