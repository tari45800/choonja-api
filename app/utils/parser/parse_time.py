import re
from datetime import datetime, timedelta

weekday_kor = {
    "월요일": 0, "화요일": 1, "수요일": 2,
    "목요일": 3, "금요일": 4, "토요일": 5, "일요일": 6
}

def get_date_by_week_offset(week_text: str, weekday_text: str) -> datetime:
    today = datetime.now()
    target_wd = weekday_kor.get(weekday_text)
    if target_wd is None:
        return None

    # 이번주 월요일
    base_monday = today - timedelta(days=today.weekday())

    # 주차 오프셋
    offset_map = {
        "저저번주": -2,
        "저번주": -1,
        "이번주": 0,
        "다음주": 1,
        "다다음주": 2
    }
    offset = offset_map.get(week_text, 0)

    # 최종 날짜
    result_date = base_monday + timedelta(weeks=offset, days=target_wd)
    return result_date

# 시간 db에 넣을 수 있게 파싱하는 함수
def parse_time(text: str) -> datetime:
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    hour, minute = 0, 0

    # 날짜 키워드 우선 처리
    if "그제" in text:
        base = now - timedelta(days=2)
        year, month, day = base.year, base.month, base.day
    elif "어제" in text:
        base = now - timedelta(days=1)
        year, month, day = base.year, base.month, base.day
    elif "내일" in text:
        base = now + timedelta(days=1)
        year, month, day = base.year, base.month, base.day
    elif "오늘" in text:
        pass
    elif m := re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text):
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    elif m := re.search(r"(\d{1,2})월\s*(\d{1,2})일", text):
        month, day = int(m.group(1)), int(m.group(2))
    else:
        # 주차+요일 먼저
        m = re.search(r"(저저번주|저번주|이번주|다음주|다다음주)\s*(월요일|화요일|수요일|목요일|금요일|토요일|일요일)", text)
        if m:
            week_text = m.group(1)
            weekday_text = m.group(2)
        else:
            # 요일만 단독
            m = re.search(r"(월요일|화요일|수요일|목요일|금요일|토요일|일요일)", text)
            if m:
                week_text = "이번주"
                weekday_text = m.group(1)
            else:
                week_text = None
                weekday_text = None

        if weekday_text:
            result = get_date_by_week_offset(week_text, weekday_text)
            if result:
                year, month, day = result.year, result.month, result.day

    # 시간대 파악
    is_am = any(x in text for x in ["오전", "새벽", "낮"])
    is_pm = any(x in text for x in ["오후", "저녁", "밤"])

    # 시, 분 추출
    if m := re.search(r"(\d{1,2})시", text):
        hour = int(m.group(1))
    if "반" in text:
        minute = 30
    elif m := re.search(r"(\d{1,2})분", text):
        minute = int(m.group(1))

    # AM/PM 보정
    if is_pm and hour < 12:
        hour += 12
    if is_am and hour == 12:
        hour = 0

    try:
        return datetime(year, month, day, hour, minute)
    except ValueError:
        return None
