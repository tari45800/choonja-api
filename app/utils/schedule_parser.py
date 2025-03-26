from datetime import datetime, timedelta, time, date
import re

# 날짜 파서
def parse_date(text: str) -> date | None:
    today = datetime.today()
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    if "오늘" in text:
        return today.date()
    elif "내일" in text:
        return (today + timedelta(days=1)).date()
    elif "모레" in text:
        return (today + timedelta(days=2)).date()

    for i, day in enumerate(weekdays):
        if f"{day}요일" in text:
            today_idx = today.weekday()
            days_ahead = (i - today_idx + 7) % 7 or 7
            return (today + timedelta(days=days_ahead)).date()

    match = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', text)
    if match:
        year, month, day = map(int, match.groups())
        return datetime(year, month, day).date()

    match = re.search(r'(\d{1,2})월\s*(\d{1,2})일', text)
    if match:
        month, day = map(int, match.groups())
        return datetime(today.year, month, day).date()

    match = re.search(r'(\d{1,2})일', text)
    if match:
        day = int(match.group(1))
        return datetime(today.year, today.month, day).date()

    return None

# 시간 파서
def parse_time(text: str) -> time | None:
    base = 0
    text = text.replace("까지", "").replace("부터", "")

    if "오전" in text or "새벽" in text:
        base = 0
    elif "오후" in text or "밤" in text or "낮" in text:
        base = 12

    # '반' 처리 (30분으로 간주)
    has_half = "반" in text
    text = text.replace("반", "")

    text = re.sub(r"(오전|오후|낮|밤|새벽)", "", text)

    match = re.search(r'(\d{1,2})시\s*(\d{1,2})?분?', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else (30 if has_half else 0)
        if hour == 12:
            hour = 0
        hour = (hour % 12) + base
        return time(hour=hour, minute=minute)

    return None


# 조사 제거 + 할 일 추출기
def parse_task_name(text: str) -> str:
    text = re.sub(r"(반|오늘|내일|모레|[월화수목금토일]요일|\d{4}년|\d{1,2}월|\d{1,2}일|오전|오후|낮|밤|새벽|\d{1,2}시\s*\d{0,2}분?|까지|부터|에서|에)", "", text)
    return text.replace(",", "").strip()

# 소요시간 파서
def parse_duration(text: str) -> int | None:
    match = re.search(r"(\\d{1,3})\\s*분\\s*(걸리(?:고|구|면|는|다|려|ㅁ)?|소요)", text)
    if match:
        return int(match.group(1))
    return None

# 통합 파서
def parse_schedule_text(text: str):
    return {
        "date": parse_date(text),
        "time": parse_time(text),
        "task": parse_task_name(text),
        "duration": parse_duration(text)
    }
