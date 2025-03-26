from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.crud.get_time_list import get_time_list
from app.utils.get_avg_interval import get_avg_interval
from app.utils.get_sleep_term import get_sleep_term

def get_parenting_report(db: Session):
    now = datetime.now()
    one_week = timedelta(days=7)
    last_week_start = now - one_week * 2
    last_week_end = now - one_week
    this_week_start = now - one_week

    def get_filtered_times(event_name: str, start_date, end_date):
        times = get_time_list(db, event_name)
        return [t for t in times if start_date <= t <= end_date]

    def get_count(event_name: str, start_date, end_date):
        times = get_time_list(db, event_name)
        return len([t for t in times if start_date <= t <= end_date])

    # 지난 주
    last_feeding = get_filtered_times("수유 시작", last_week_start, last_week_end)
    last_diaper = get_filtered_times("기저귀 교체", last_week_start, last_week_end)
    last_sleep_start = get_filtered_times("애기 수면 시작", last_week_start, last_week_end)
    last_sleep_end = get_filtered_times("애기 수면 끝", last_week_start, last_week_end)
    last_week_formula = get_count("분유 수유", last_week_start, last_week_end)
    last_week_diaper = get_count("기저귀 교체", last_week_start, last_week_end)

    # 이번 주
    this_feeding = get_filtered_times("수유 시작", this_week_start, now)
    this_diaper = get_filtered_times("기저귀 교체", this_week_start, now)
    this_sleep_start = get_filtered_times("애기 수면 시작", this_week_start, now)
    this_sleep_end = get_filtered_times("애기 수면 끝", this_week_start, now)
    this_week_formula = get_count("분유 수유", this_week_start, now)
    this_week_diaper = get_count("기저귀 교체", this_week_start, now)

    # 평균 텀 계산
    last_feeding_term = get_avg_interval(last_feeding)
    this_feeding_term = get_avg_interval(this_feeding)
    last_diaper_term = get_avg_interval(last_diaper)
    this_diaper_term = get_avg_interval(this_diaper)
    last_sleep_term = get_sleep_term(last_sleep_start, last_sleep_end)
    this_sleep_term = get_sleep_term(this_sleep_start, this_sleep_end)

    # 차이 계산
    feeding_diff = this_feeding_term - last_feeding_term if last_feeding_term and this_feeding_term else None
    diaper_diff = this_diaper_term - last_diaper_term if last_diaper_term and this_diaper_term else None
    sleep_diff = this_sleep_term - last_sleep_term if last_sleep_term and this_sleep_term else None

    def fmt(minutes):
        if minutes is None:
            return "데이터 부족"
        h = int(minutes // 60)
        m = int(minutes % 60)
        if h and m: return f"{h}시간 {m}분"
        elif h: return f"{h}시간"
        else: return f"{m}분"

    def safe_diff_message(diff, up_msg, down_msg, default):
        if diff is None:
            return default
        return up_msg if diff > 0 else down_msg

    def count_change(now_count, last_count, item_name):
        diff = now_count - last_count
        if diff == 0:
            return f"{item_name} 사용량은 지난 주와 같아요."
        elif diff > 0:
            return f"{item_name} 사용량이 지난 주보다 {diff}개 늘었어요."
        else:
            return f"{item_name} 사용량이 지난 주보다 {abs(diff)}개 줄었어요."

    # 문장 정리
    time_briefing = (
        f"지난 주 평균 수유 간격은 {fmt(last_feeding_term)}였고, 이번 주는 {fmt(this_feeding_term)}로 "
        f"{safe_diff_message(feeding_diff, '늘었어요', '줄었어요', '비교할 수 없어요')}."
        f"기저귀는 지난 주 {fmt(last_diaper_term)}, 이번 주 {fmt(this_diaper_term)}로 "
        f"{safe_diff_message(diaper_diff, '간격이 길어졌어요', '짧아졌어요', '비교할 수 없어요')}."
        f"수면 간격은 지난 주 {fmt(last_sleep_term)}, 이번 주 {fmt(this_sleep_term)}로 "
        f"{safe_diff_message(sleep_diff, '길어졌어요', '짧아졌어요', '비교할 수 없어요')}."
    )

    stock_briefing = (
        f"분유는 지난 주 {last_week_formula}개, 이번 주 {this_week_formula}개 사용했어요. "
        f"{count_change(this_week_formula, last_week_formula, '분유')}"
        f"기저귀는 지난 주 {last_week_diaper}개, 이번 주 {this_week_diaper}개 사용했어요. "
        f"{count_change(this_week_diaper, last_week_diaper, '기저귀')}"
    )

    return {
        "message": time_briefing + stock_briefing
    }
