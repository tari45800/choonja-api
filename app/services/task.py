from sqlalchemy.orm import Session
from app.utils.parser.split_time import split_time
from app.utils.parser.parse_time import parse_time
from app.utils.parser.parse_action import parse_action


def create_task_service(text: str, db: Session):
    # 1. 시간/행동 분리
    time_part, action_part = split_time(text)

    # 2. 시간 파싱
    dt = parse_time(time_part) if time_part else None
    ac = parse_action(action_part) if action_part else None

    # 3. 확인용 출력
    print("📥 입력된 텍스트:", text)
    print("🕒 시간 표현:", time_part)
    print("🎯 행동 표현:", action_part)
    print("📅 파싱된 datetime:", dt)
    print("📅 파싱된 datetime:", ac)

    # 4. 일단 테스트니까 리턴만 해보자
    return {
        "text": text,
        "time_part": time_part,
        "action_part": action_part,
        "datetime": dt.isoformat() if dt else None
    }
