from typing import List
from datetime import datetime

def get_sleep_term(start_times: List[datetime], end_times: List[datetime]) -> float:
    # 정렬해서 짝 맞추기
    start_times.sort()
    end_times.sort()

    # 수면 간격 쌍 만들기
    pairs = []
    for i in range(1, min(len(start_times), len(end_times))):
        prev_end = end_times[i - 1]
        next_start = start_times[i]
        if next_start > prev_end:
            pairs.append((prev_end, next_start))

    if not pairs:
        return 0.0  # 데이터 없으면 0분 처리

    # 평균 간격 계산
    total_seconds = sum((s - e).total_seconds() for e, s in pairs)
    avg_minutes = total_seconds / 60 / len(pairs)

    return avg_minutes
