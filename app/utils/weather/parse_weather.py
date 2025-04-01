# app/utils/weather/parser.py

import arrow
from app.utils.weather.fetch_weather import SKY_STATUS, PTY_STATUS

def parse_items_to_current_weather(items: list, location: str = "부산 수영구"):
    now = arrow.now("Asia/Seoul")
    current_time = now.format("HHmm")

    # 가장 가까운 시간대 기준 필터링
    closest = {}
    tmx = None
    tmn = None

    for item in items:
        category = item["category"]
        fcst_time = item["fcstTime"]

        # 최고/최저기온 따로 저장
        if category == "TMX":
            tmx = item["fcstValue"]
        elif category == "TMN":
            tmn = item["fcstValue"]

        # 현재 시각 기준 가장 가까운 시간대만 추출
        if fcst_time >= current_time and category in ["TMP", "SKY", "PTY", "PCP", "WSD"]:
            if category not in closest:
                closest[category] = item["fcstValue"]

    # SKY, PTY 코드 → 한글 변환
    sky_text = SKY_STATUS.get(closest.get("SKY", "1"), "맑음")
    rain_text = PTY_STATUS.get(closest.get("PTY", "0"), "비 안옴")

    # 강수량 처리
    pcp = closest.get("PCP", "강수없음")
    if pcp == "강수없음" or pcp == "강수 없음":
        pcp_val = "강수없음"
    elif pcp == "1mm 미만":
        pcp_val = "0.5mm"
    else:
        pcp_val = pcp

    return {
        "location": location,
        "temp": closest.get("TMP", "?"),
        "highest": tmx or closest.get("TMP", "?"),
        "lowest": tmn or closest.get("TMP", "?"),
        "sky": sky_text,
        "rain": rain_text,
        "pcp": pcp_val,
        "wsd": closest.get("WSD", "0")
    }
