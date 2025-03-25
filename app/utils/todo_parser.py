import re
from datetime import datetime, timedelta

def custom_date_parser(text: str):
    today = datetime.today()
    original = text.strip()
    parsed_date = None
    task_name = original

    # ✅ 조사 패턴
    def clean_task_name(text, keyword):
        # '내일에 예방접종' → '예방접종'으로 정리
        return re.sub(rf"{keyword}(에|에서|까지|부터)?", "", text).strip()

    # 1. 오늘 / 내일 / 모레
    if "오늘" in text:
        parsed_date = today
        task_name = clean_task_name(text, "오늘")
    elif "내일" in text:
        parsed_date = today + timedelta(days=1)
        task_name = clean_task_name(text, "내일")
    elif "모레" in text:
        parsed_date = today + timedelta(days=2)
        task_name = clean_task_name(text, "모레")

    # 2. 요일 처리
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    for i, day in enumerate(weekdays):
        if day + "요일" in text:
            today_idx = today.weekday()
            target_idx = i
            days_ahead = (target_idx - today_idx + 7) % 7 or 7
            parsed_date = today + timedelta(days=days_ahead)
            task_name = clean_task_name(text, day + "요일")
            break

    # 3. YYYY년 MM월 DD일
    match = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', text)
    if match:
        year, month, day = map(int, match.groups())
        parsed_date = datetime(year, month, day)
        task_name = clean_task_name(text, match.group())

    # 4. MM월 DD일
    if not parsed_date:
        match = re.search(r'(\d{1,2})월\s*(\d{1,2})일', text)
        if match:
            month, day = map(int, match.groups())
            parsed_date = datetime(today.year, month, day)
            task_name = clean_task_name(text, match.group())

    # 5. DD일만 있는 경우
    if not parsed_date:
        match = re.search(r'(\d{1,2})일', text)
        if match:
            day = int(match.group(1))
            parsed_date = datetime(today.year, today.month, day)
            task_name = clean_task_name(text, match.group())

    return parsed_date.date() if parsed_date else None, task_name
