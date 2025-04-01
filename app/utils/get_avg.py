from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from app.models import Schedule

# 실제 기록 시각으로 변환
def to_schedule_datetime(s: Schedule) -> datetime:
    return datetime(
        year=s.year,
        month=int(s.month),
        day=int(s.day),
        hour=s.time.hour if s.time else 0,
        minute=s.time.minute if s.time else 0,
        second=s.time.second if s.time else 0,
    )


# 단일 기록 평균 텀
def get_avg_interval(records: List[Schedule]) -> timedelta:
    if len(records) < 2:
        return timedelta(0)

    records = sorted(records, key=lambda r: to_schedule_datetime(r))
    intervals = [
        to_schedule_datetime(records[i]) - to_schedule_datetime(records[i - 1])
        for i in range(1, len(records))
    ]

    # 전체 평균 timedelta
    avg_timedelta = sum(intervals, timedelta()) / len(intervals)

    # ⏱ 초 단위 → 분 단위로 반올림
    total_seconds = avg_timedelta.total_seconds()
    rounded_minutes = round(total_seconds / 60)

    return timedelta(minutes=rounded_minutes)

# 수면 페어 객체 배열 만들기
def get_sleep_pairs(start_records: List[Schedule], end_records: List[Schedule]) -> List[Dict[str, datetime]]:
    all_records = start_records + end_records
    all_records.sort(key=to_schedule_datetime)

    pairs = []
    i = 0
    while i < len(all_records) - 1:
        cur = all_records[i]
        nxt = all_records[i + 1]

        if cur.action.name == "애기 수면 시작" and nxt.action.name == "애기 수면 종료":
            pairs.append({
                "start": to_schedule_datetime(cur),
                "end": to_schedule_datetime(nxt)
            })
            i += 2
        else:
            i += 1

    return pairs

# 수면 시간 구하기
def get_sleep_durations(sleep_pairs: List[dict]) -> List[timedelta]:
    durations = []
    for i, pair in enumerate(sleep_pairs):
        start = pair["start"]
        end = pair["end"]
        if end > start:
            duration = end - start
            durations.append(duration)
        else:
            print(f"⚠️ 페어 #{i+1}: 종료 시간이 시작 시간보다 빠름 → 스킵")
    return durations

# 수면 사이클 간격 구하기
def get_sleep_cycle_intervals(sleep_pairs: List[dict]) -> List[timedelta]:
    cycle_intervals = []
    for i in range(len(sleep_pairs) - 1):
        prev_end = sleep_pairs[i]["end"]
        next_start = sleep_pairs[i + 1]["start"]

        if next_start > prev_end:
            gap = next_start - prev_end
            cycle_intervals.append(gap)
        else:
            print(f"⚠️ 페어 #{i+1} → #{i+2}: 시작 시간이 이전 종료보다 빠름 → 스킵")

    return cycle_intervals

# 수면 시간/사이클 평균까지 계산
def get_sleep_stats(
    start_records: List[Schedule],
    end_records: List[Schedule]
) -> Tuple[List[timedelta], List[timedelta], timedelta, timedelta]:
    sleep_pairs = get_sleep_pairs(start_records, end_records)
    durations = get_sleep_durations(sleep_pairs)
    cycles = get_sleep_cycle_intervals(sleep_pairs)

    avg_duration = sum(durations, timedelta()) / len(durations) if durations else timedelta(0)
    avg_cycle = sum(cycles, timedelta()) / len(cycles) if cycles else timedelta(0)

    return durations, cycles, avg_duration, avg_cycle
