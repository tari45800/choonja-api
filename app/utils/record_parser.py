import re
from datetime import datetime, timedelta, time

def parse_record_text(text: str) -> dict:
    now = datetime.now()
    task_name = text.strip()
    record_datetime = now

    # 1. "1시간 30분 전", "2시간 10분 전" 같이 복합 시간
    match = re.search(r"(\d{1,2})시간\s*(\d{1,2})?분?\s*전", text)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2) or 0)
        record_datetime = now - timedelta(hours=hours, minutes=minutes)
        task_name = re.sub(r"\d{1,2}시간\s*\d{0,2}분?\s*전(에)?", "", text).strip()

    # 2. "30분 전", "2시간 전에"
    elif re.search(r"(\d{1,2})\s*(분|시간)\s*전", text):
        match = re.search(r"(\d{1,2})\s*(분|시간)\s*전", text)
        amount = int(match.group(1))
        unit = match.group(2)
        if unit == "분":
            record_datetime = now - timedelta(minutes=amount)
        elif unit == "시간":
            record_datetime = now - timedelta(hours=amount)
        task_name = re.sub(r"\d{1,2}\s*(분|시간)\s*전(에)?", "", text).strip()

    # 3. 절대시간: "1시", "2시 반", "3시 30분"
    else:
        match = re.search(r"(\d{1,2})시\s*(반|\d{1,2})?(분)?", text)
        if match:
            hour = int(match.group(1))
            minute = 30 if match.group(2) == "반" else int(match.group(2) or 0)
            record_datetime = datetime.combine(now.date(), time(hour=hour, minute=minute))
            task_name = re.sub(r"\d{1,2}시\s*(반|\d{1,2})?(분)?(에)?", "", text).strip()

    # 4. 완료형 어미 제거
    task_name = re.sub(r"(했어|었어|았어|였다|였다가|갔어|왔다|먹었어|마셨어|봤어|잤어|좋아)", "", task_name).strip()

    # 5. 특수 키워드 텍스트 변환
    if "기저귀" in task_name and "샀" in text:
        task_name = "기저귀 구매"
    elif "기저귀" in task_name:
        task_name = "기저귀 교체"

    return {
        "date": record_datetime.date(),
        "time": record_datetime.time(),
        "task": task_name
    }
