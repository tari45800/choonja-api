from collections import defaultdict

TIME_BLOCKS = {
    "새벽": range(0, 6),
    "아침": range(6, 9),
    "점심": range(9, 14),
    "저녁": range(14, 19),
    "밤": range(19, 24),
}

BLOCK_START_HOUR = {
    "새벽": 0,
    "아침": 6,
    "점심": 9,
    "저녁": 14,
    "밤": 19,
}

def generate_timeblock_temp_briefing(tmp_list: list, current_hour: int, current_month: int) -> dict:
    def get_season(month: int) -> str:
        if 3 <= month <= 4:
            return "spring"
        elif 5 <= month <= 9:
            return "summer"
        elif month == 10:
            return "fall"
        else:
            return "winter"

    TEMP_FEELING = {
        "spring": [(-100, "매우 추운 날씨입니다."), (0, "추운 날씨입니다."), (5, "쌀쌀한 날씨입니다."),
                   (10, "선선한 날씨입니다."), (15, "온화한 날씨입니다."), (20, "따뜻한 날씨입니다."), (25, "더운 날씨입니다.")],
        "summer": [(-100, "서늘한 날씨입니다."), (20, "쾌적한 날씨입니다."), (25, "더운 날씨입니다."),
                   (30, "무더운 날씨입니다."), (33, "폭염 수준의 날씨입니다.")],
        "fall":   [(-100, "매우 추운 날씨입니다."), (0, "추운 날씨입니다."), (5, "쌀쌀한 날씨입니다."),
                   (10, "선선한 날씨입니다."), (15, "온화한 날씨입니다."), (20, "따뜻한 날씨입니다."), (25, "더운 날씨입니다.")],
        "winter": [(-100, "매우 추운 날씨입니다."), (0, "추운 날씨입니다."), (5, "쌀쌀한 날씨입니다."),
                   (10, "겨울치곤 온화한 날씨입니다.")]
    }

    def get_temp_feeling(temp: float, season: str) -> str:
        for threshold, feeling in reversed(TEMP_FEELING[season]):
            if temp >= threshold:
                return feeling
        return "정보 없음"

    season = get_season(current_month)
    block_temps = defaultdict(list)

    for time_str, temp_str in tmp_list:
        hour = int(time_str[:2])
        temp = float(temp_str)
        for block_name, hours in TIME_BLOCKS.items():
            if hour in hours:
                block_temps[block_name].append(temp)
                break

    result = {}
    for block, temps in block_temps.items():
        if BLOCK_START_HOUR[block] >= current_hour:
            avg = sum(temps) / len(temps)
            feeling = get_temp_feeling(avg, season)
            result[block] = (round(avg, 1), feeling)

    return result


def generate_temp_feeling_sentence(temp_blocks: dict) -> str:
    if not temp_blocks:
        return "시간대별 기온 정보가 부족합니다."

    def format_hour(hour: int) -> str:
        if hour < 12:
            return f"오전 {hour}시 이후로는"
        elif hour == 12:
            return "정오 이후로는"
        else:
            return f"오후 {hour - 12}시 이후로는"

    sorted_blocks = ["새벽", "아침", "점심", "저녁", "밤"]
    visible_blocks = [b for b in sorted_blocks if b in temp_blocks]

    parts = []
    for block in visible_blocks:
        avg, feeling = temp_blocks[block]
        hour = BLOCK_START_HOUR[block]
        time_phrase = format_hour(hour)
        parts.append(f"{time_phrase} 평균 {avg}도로 {feeling}")

    return " ".join(parts)
