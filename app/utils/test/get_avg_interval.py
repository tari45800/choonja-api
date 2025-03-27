from datetime import datetime

def get_avg_interval(time_list: list[datetime]) -> float:
    if len(time_list) < 2:
        return 0.0  # 데이터가 부족할 땐 0.0으로 처리 (None으로 바꿔도 됨)

    total_seconds = 0
    for i in range(1, len(time_list)):
        diff = (time_list[i] - time_list[i - 1]).total_seconds()
        total_seconds += diff

    avg_seconds = total_seconds / (len(time_list) - 1)
    avg_minutes = avg_seconds / 60  # 초 → 분 변환

    return avg_minutes
