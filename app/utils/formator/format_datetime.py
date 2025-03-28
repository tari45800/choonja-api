from datetime import datetime, timedelta

def format_datetime(dt: datetime) -> str:
    now = datetime.now()
    today = now.date()
    delta = (dt.date() - today).days

    include_time = dt.time() != datetime.min.time()  # 00:00:00이 아니면 시간 포함

    # 날짜는 무조건 표현
    if delta == 0:
        date_str = "오늘"
    elif delta == 1:
        date_str = "내일"
    elif delta == 2:
        date_str = "모레"
    elif delta == -1:
        date_str = "어제"
    elif delta == -2:
        date_str = "그제"
    else:
        date_str = f"{dt.year}년 {dt.month}월 {dt.day}일"

    # 시간 표현
    time_str = ""
    if include_time:
        hour = dt.hour
        minute = dt.minute

        if hour < 6:
            ampm = "새벽"
        elif hour < 12:
            ampm = "오전"
        elif hour < 18:
            ampm = "오후"
            hour -= 12 if hour > 12 else 0
        else:
            ampm = "저녁"
            hour -= 12 if hour > 12 else 0

        if minute == 0:
            time_str = f"{ampm} {hour}시"
        else:
            time_str = f"{ampm} {hour}시 {minute}분"

    # 조합
    if include_time:
        return f"{date_str} {time_str}"
    else:
        return date_str
