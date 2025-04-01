from datetime import datetime, timedelta
from app.crud.record import get_records_grouped_by_action, get_latest_record_by_action_name
from app.utils.get_avg import (
    get_avg_interval,
    get_sleep_stats,
    to_schedule_datetime
)
from app.utils.get_reason import get_predicted_crying_reason  # ✅ 추가!

def crying_event_service(db):
    now = datetime.now()
    start = now - timedelta(days=7)
    end = now

    # ✅ 1. 기록 가져오기
    records = get_records_grouped_by_action(
        db,
        ["기저귀 교체", "수유", "애기 수면 시작", "애기 수면 종료"],
        start,
        end
    )

    # ✅ 2. 평균 텀 계산
    diaper_avg = get_avg_interval(records["기저귀 교체"])
    feeding_avg = get_avg_interval(records["수유"])
    sleep_durations, sleep_cycles, sleep_avg_duration, sleep_avg_cycle = get_sleep_stats(
        records["애기 수면 시작"], records["애기 수면 종료"]
    )

    # ✅ 3. 최신 기록 가져오기
    latest_diaper = get_latest_record_by_action_name("기저귀 교체", db)
    latest_feeding = get_latest_record_by_action_name("수유", db)
    latest_sleep_start = get_latest_record_by_action_name("애기 수면 시작", db)
    latest_sleep_end = get_latest_record_by_action_name("애기 수면 종료", db)

    # ✅ 4. 시간 경과 비율 계산
    def get_ratio_since_latest(latest, avg):
        if not latest or avg.total_seconds() == 0:
            return None
        elapsed = now - to_schedule_datetime(latest)
        return round((elapsed / avg) * 100)

    diaper_ratio = get_ratio_since_latest(latest_diaper, diaper_avg)
    feeding_ratio = get_ratio_since_latest(latest_feeding, feeding_avg)
    sleep_ratio = get_ratio_since_latest(latest_sleep_start, sleep_avg_cycle)
    wake_ratio = get_ratio_since_latest(latest_sleep_end, sleep_avg_duration)

    # ✅ 5. 예측용 딕셔너리 정리
    latest_dict = {
        "diaper": to_schedule_datetime(latest_diaper) if latest_diaper else None,
        "feeding": to_schedule_datetime(latest_feeding) if latest_feeding else None,
        "sleep": to_schedule_datetime(latest_sleep_start) if latest_sleep_start else None,
        "wake": to_schedule_datetime(latest_sleep_end) if latest_sleep_end else None,
    }

    avg_dict = {
        "diaper": diaper_avg,
        "feeding": feeding_avg,
        "sleep": sleep_avg_cycle,
        "wake": sleep_avg_duration,
    }

    ratio_dict = {
        "diaper": diaper_ratio,
        "feeding": feeding_ratio,
        "sleep": sleep_ratio,
        "wake": wake_ratio,
    }

    print("🧪 feeding_avg:", feeding_avg)
    print("🧪 latest_feeding:", latest_feeding)
    print("🧪 feeding_ratio:", feeding_ratio)

    # ✅ 6. 울음 예측 메시지 생성
    reason_message = get_predicted_crying_reason(now, latest_dict, avg_dict, ratio_dict)

    return {
        "message": reason_message
    }
