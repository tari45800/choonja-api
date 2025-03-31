from app.utils.parser.split_time import split_time
from app.utils.parser.parse_time import parse_time
from app.utils.parser.parse_action import parse_action

def extract_parts(text: str):
    time_part, action_part = split_time(text)
    dt = parse_time(time_part) if time_part else None
    an = parse_action(action_part) if action_part else None

    if not an:
        return {
            "result": None,
            "message": "인식할 수 없는 명령어 입니다."
        }

    return {
        "dt": dt,
        "action": an
    }
