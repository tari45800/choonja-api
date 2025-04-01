from datetime import datetime, timedelta

def get_predicted_crying_reason(
    now: datetime,
    latest: dict,
    avg: dict,
    ratio: dict
) -> str:
    reasons = [
        ("기저귀를 갈아야 해서 울었어요.", "diaper"),
        ("밥을 먹어야 해서 울었어요.", "feeding"),
        ("잠을 자야 해서 울었어요.", "sleep"),
        ("깰 때가 돼서 울었어요.", "wake")
    ]

    # 비율 기준으로 정렬
    sorted_reasons = sorted(
        [(label, key, ratio.get(key)) for label, key in reasons if ratio.get(key) is not None],
        key=lambda x: x[2], reverse=True
    )

    lines = []
    for idx, (label, key, r) in enumerate(sorted_reasons[:4]):
        minutes_elapsed = int((now - latest[key]).total_seconds() / 60) if latest[key] else "?"
        avg_minutes = int(avg[key].total_seconds() / 60) if avg[key] else "?"

        if idx == 0:
            lines.append(f"울음 예상 원인은 {label} ")
        else:
            lines.append(f"다음 예상 원인은 {label} ")

        lines.append(f"마지막으로 기록으로부터 약 {minutes_elapsed}분 지났고, 지난주 평균 주기는 {avg_minutes}분입니다.")

    return "".join(lines)
