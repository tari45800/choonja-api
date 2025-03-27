from datetime import date, timedelta

def get_relative_day_label(target_date: date) -> str:
    today = date.today()
    diff = (target_date - today).days

    if diff == 0:
        return "오늘"
    elif diff == 1:
        return "내일"
    elif diff == 2:
        return "모레"
    else:
        return target_date.strftime("%Y-%m-%d") 
