import arrow

def get_rain_strength(pcp_val: float) -> str:
    """
    강수량 값(mm)에 따른 설명을 정돈된 톤으로 반환
    """
    if pcp_val == 0:
        return "비는 내리지 않겠습니다."
    elif pcp_val < 1:
        return "가랑비가 조금 내릴 것으로 보입니다."
    elif pcp_val < 5:
        return "약한 비가 예상됩니다."
    elif pcp_val < 20:
        return "비가 다소 내릴 것으로 보입니다."
    elif pcp_val < 50:
        return "장대비가 예상됩니다."
    else:
        return "폭우가 내릴 가능성이 높습니다."

def get_wind_strength(wsd_val: float) -> str:
    """
    풍속 값(m/s)에 따른 설명을 정돈된 톤으로 반환
    """
    if wsd_val < 4:
        return "바람은 거의 불지 않겠습니다."
    elif wsd_val < 7:
        return "바람이 약간 불겠습니다."
    elif wsd_val < 10:
        return "바람이 다소 강하게 불겠습니다."
    else:
        return "강한 바람이 불겠습니다."

def get_today_tmp_pcp_list(items: list):
    """
    기상청 예보 항목 중 오늘 날짜 기준 TMP, PCP 데이터만 정리
    """
    today = arrow.now("Asia/Seoul").format("YYYYMMDD")
    tmp_data = []
    pcp_data = []

    for item in items:
        if item["fcstDate"] != today:
            continue
        category = item["category"]
        time = item["fcstTime"]
        value = item["fcstValue"]

        if category == "TMP":
            tmp_data.append((time, value))
        elif category == "PCP":
            pcp_data.append((time, value))

    # 시간순 정렬
    tmp_data.sort()
    pcp_data.sort()

    return tmp_data, pcp_data

