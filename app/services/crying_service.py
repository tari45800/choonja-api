from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.event_stats import get_weekly_event_counts
from app.utils.get_avg_interval import get_avg_interval
from app.utils.get_sleep_term import get_sleep_term
from app.crud.get_time_list import get_time_list

def handle_crying_event_service(db: Session):
    now = datetime.now()
    stats = get_weekly_event_counts(db)

    def get_elapsed_minutes(last_time):
        return (now - last_time).total_seconds() / 60 if last_time else None

    def calculate_score(elapsed, avg):
        if elapsed is None or avg is None:
            return None
        if elapsed < avg:
            return 1 - (avg - elapsed) / avg
        else:
            return 1 + (elapsed - avg) / avg

    def minutes_to_korean(minutes: float) -> str:
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if hours and mins:
            return f"{hours}시간 {mins}분"
        elif hours:
            return f"{hours}시간"
        else:
            return f"{mins}분"

    # 수유
    feeding_times = get_time_list(db, "수유 시작")
    feeding_term = float(get_avg_interval(feeding_times)) if feeding_times else None
    feeding_elapsed = get_elapsed_minutes(feeding_times[-1]) if feeding_times else None
    feeding_score = calculate_score(feeding_elapsed, feeding_term)

    # 기저귀
    diaper_times = get_time_list(db, "기저귀 교체")
    diaper_term = float(get_avg_interval(diaper_times)) if diaper_times else None
    diaper_elapsed = get_elapsed_minutes(diaper_times[-1]) if diaper_times else None
    diaper_score = calculate_score(diaper_elapsed, diaper_term)

    # 수면
    sleep_starts = get_time_list(db, "애기 수면 시작")
    sleep_ends = get_time_list(db, "애기 수면 끝")
    sleep_term = float(get_sleep_term(sleep_starts, sleep_ends)) if sleep_starts and sleep_ends else None
    sleep_elapsed = get_elapsed_minutes(sleep_ends[-1]) if sleep_ends else None
    sleep_score = calculate_score(sleep_elapsed, sleep_term)

    # 예측 원인 순위
    reasons = []
    if feeding_score is not None:
        reasons.append(("수유", feeding_score))
    if sleep_score is not None:
        reasons.append(("낮잠", sleep_score))
    if diaper_score is not None:
        reasons.append(("기저귀", diaper_score))

    reasons.sort(key=lambda x: x[1], reverse=True)
    ranked_reasons = [r[0] for r in reasons]

    # 시리용 문장 생성
    def make_voice_summary():
        lines = ["아이가 울고 있어요."]
        for i, reason in enumerate(ranked_reasons):
            prefix = f"예측 원인 {i+1}위는 {reason}입니다."
            if reason == "수유":
                lines.append(
                    f"{prefix} 수유한 지 {minutes_to_korean(feeding_elapsed)} 지났고, 평균 수유 간격은 {minutes_to_korean(feeding_term)}예요."
                )
            elif reason == "낮잠":
                lines.append(
                    f"{prefix} 마지막 낮잠 후 {minutes_to_korean(sleep_elapsed)} 지났고, 평균 낮잠 간격은 {minutes_to_korean(sleep_term)}예요."
                )
            elif reason == "기저귀":
                lines.append(
                    f"{prefix} 기저귀 갈아준 지 {minutes_to_korean(diaper_elapsed)} 지났고, 평균 기저귀 간격은 {minutes_to_korean(diaper_term)}예요."
                )
        return " ".join(lines)

    voice_message = make_voice_summary()

    return {
        "message": voice_message,
        # "summary": {
        #     "수유": {
        #         "횟수": stats.get("feeding", 0),
        #         "평균 텀(분)": round(feeding_term, 1) if feeding_term else None,
        #         "지난 수유 후 경과 시간(분)": round(feeding_elapsed, 1) if feeding_elapsed else None
        #     },
        #     "기저귀": {
        #         "횟수": stats.get("diaper", 0),
        #         "평균 텀(분)": round(diaper_term, 1) if diaper_term else None,
        #         "지난 기저귀 교체 후 경과 시간(분)": round(diaper_elapsed, 1) if diaper_elapsed else None
        #     },
        #     "낮잠": {
        #         "횟수": stats.get("sleep", 0),
        #         "평균 텀(분)": round(sleep_term, 1) if sleep_term else None,
        #         "지난 낮잠 후 경과 시간(분)": round(sleep_elapsed, 1) if sleep_elapsed else None
        #     }
        # },
        # "prediction": [f"{i+1}위 {r}" for i, r in enumerate(ranked_reasons)]
    }
