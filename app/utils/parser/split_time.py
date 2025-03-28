import re

# 시간과 목적을 분리하는 함수
def split_time(text: str):
    pattern = r"(\d{4}년\s*\d{1,2}월\s*\d{1,2}일|\d{1,2}월\s*\d{1,2}일|\d{1,2}시\s*반|\d{1,2}시\s*\d{1,2}분|\d{1,2}시|오늘|내일|어제|그제|오전|오후|밤|저녁|새벽|낮|다음주|이번주|저번주|[월화수목금토일]요일)"

    matches = list(re.finditer(pattern, text))

    if not matches:
        return None, text.strip()

    last = matches[-1]
    cut = last.end()

    time_part = text[:cut].strip()
    action_part = text[cut:].strip()

    return time_part, action_part
