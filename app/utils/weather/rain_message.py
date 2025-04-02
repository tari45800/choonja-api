from collections import defaultdict

TIME_BLOCKS = {
    "새벽": range(0, 6),
    "아침": range(6, 9),
    "점심": range(9, 14),
    "저녁": range(14, 19),
    "밤": range(19, 24),
}

def summarize_rain_by_timeblock(pcp_list: list) -> dict:
    """
    [('0300', '강수없음'), ('0600', '1.2'), ...] 형태의 강수 데이터 → 시간대별 평균 mm
    """
    block_rain = defaultdict(list)

    for time_str, pcp in pcp_list:
        hour = int(time_str[:2])

        # 값 정제
        if "강수없음" in pcp or pcp.strip() == "":
            mm = 0
        elif "mm 미만" in pcp:
            mm = 0.5
        else:
            try:
                mm = float(pcp.replace("mm", "").strip())
            except:
                mm = 0

        # 시간대 분류
        for block, hours in TIME_BLOCKS.items():
            if hour in hours:
                block_rain[block].append(mm)
                break

    # 평균 계산
    result = {}
    for block, vals in block_rain.items():
        avg = sum(vals) / len(vals)
        result[block] = round(avg, 1)

    return result

def generate_rain_message_by_timeblock(block_mm_dict: dict) -> str:
    def classify_rain(mm: float) -> str:
        if mm == 0:
            return None
        elif mm < 1:
            return "가랑비가 조금"
        elif mm < 5:
            return "약한 비가"
        elif mm < 20:
            return "비가 다소"
        elif mm < 50:
            return "강한 비가"
        else:
            return "폭우가"

    sorted_blocks = ["새벽", "아침", "점심", "저녁", "밤"]
    phrases = []

    for block in sorted_blocks:
        mm = block_mm_dict.get(block)
        label = classify_rain(mm) if mm is not None else None
        if label:
            phrases.append(f"{block}에는 {label} 예상됩니다")

    if not phrases:
        return "오늘 하루 동안 비 소식은 없겠습니다."
    elif len(phrases) == 1:
        return f"{phrases[0]}."
    else:
        return ", ".join(phrases[:-1]) + f", 그리고 {phrases[-1]}."
