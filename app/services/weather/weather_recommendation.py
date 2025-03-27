import arrow

def recommend_outfit(temp_c, tmx, tmn, month):
    temp = float(temp_c)
    tmx = float(tmx)
    tmn = float(tmn)
    daily_gap = tmx - tmn
    outfit = ""
    outer = ""

    # 겉옷 여부 판단
    if daily_gap >= 10:
        outer = "일교차가 커서 겉옷이 필요해요."

    # 계절 구분
    if 3 <= month <= 4:
        season = "봄"
    elif 5 <= month <= 9:
        season = "여름"
    elif month == 10:
        season = "가을"
    else:
        season = "겨울"

    # 계절 + 기온 조합별 추천 멘트
    if season == "봄":
        if temp <= 9:
            outfit = "겨울처럼 쌀쌀해요. 두꺼운 외투를 입으세요."
        elif temp <= 20:
            outfit = "얇은 긴팔과 바지가 적당해요."
        else:
            outfit = "따뜻한 날씨예요. 반팔도 괜찮아요."
    elif season == "여름":
        if temp <= 20:
            outfit = "조금 선선해요. 얇은 겉옷 챙기세요."
        elif temp <= 30:
            outfit = "반팔, 반바지 딱 좋아요."
        else:
            outfit = "매우 더워요. 통풍 잘 되는 옷이 좋아요."
    elif season == "가을":
        if temp <= 9:
            outfit = "초겨울처럼 추워요. 따뜻하게 입으세요."
        elif temp <= 20:
            outfit = "긴팔과 가벼운 겉옷이 좋아요."
        else:
            outfit = "포근해요. 반팔도 괜찮아요."
    elif season == "겨울":
        if temp <= 4:
            outfit = "매우 추워요. 패딩과 목도리 필수예요."
        elif temp <= 9:
            outfit = "쌀쌀해요. 따뜻한 외투 챙기세요."
        else:
            outfit = "겨울치고 따뜻해요. 가벼운 외투도 OK."

    return f"{outfit} {outer}".strip()

def recommend_items(sky, rain, pcp, wsd):
    """
    Siri가 읽을 준비물 추천 멘트를 생성합니다.
    """
    items = []

    # 강수량 숫자로 변환
    try:
        if "강수없음" in pcp:
            pcp_val = 0
        elif "미만" in pcp:
            pcp_val = float(pcp.replace("mm 미만", "").strip()) or 0.5
        else:
            pcp_val = float(pcp.replace("mm", "").strip())
    except:
        pcp_val = 0

    # 풍속 숫자로 변환
    try:
        wind = float(wsd)
    except:
        wind = 0

    # ☀️ 햇빛 대비
    if sky == "맑음":
        items.append("양산")
        if wind >= 5:
            items.append("모자")

    # 🌧️ 비 대비
    if rain in ["비", "비/눈", "소나기", "눈"]:
        if pcp_val >= 20 and wind >= 5:
            items += ["우비", "장화"]
        elif pcp_val >= 5:
            items += ["우산", "장화"]
        else:
            items.append("우산")

    # 🌬️ 흐리고 바람 많을 때
    if sky in ["흐림", "구름 많음"] and wind >= 5:
        items.append("바람막이")

    if not items:
        return "특별히 챙길 준비물은 없어요."

    # Siri가 자연스럽게 읽을 수 있게 구성
    if len(items) == 1:
        return f"{items[0]} 하나 챙기면 좋겠어요."
    elif len(items) == 2:
        return f"{items[0]}와 {items[1]} 챙기면 좋겠어요."
    else:
        return f"{', '.join(items[:-1])} 그리고 {items[-1]} 챙기면 좋겠어요."

def get_weather_briefing(weather_data):
    import arrow

    temp = weather_data.get("temp") or weather_data.get("highest")
    highest = weather_data.get("highest") or temp or "?"
    lowest = weather_data.get("lowest") or temp or "?"

    try:
        outfit = recommend_outfit(
            temp_c=temp,
            tmx=highest,
            tmn=lowest,
            month=arrow.now().month
        )
    except ValueError:
        outfit = "옷차림 정보를 불러올 수 없어요."

    items = recommend_items(
        sky=weather_data.get("sky"),
        rain=weather_data.get("rain"),
        pcp=weather_data.get("pcp", "강수없음"),
        wsd=weather_data.get("wsd", "0")
    )

    return (
        f"{weather_data.get('location')} 날씨는 {weather_data.get('sky')}이고 {weather_data.get('rain')}이에요. "
        f"최고 기온은 {highest}도, 최저 기온은 {lowest}도예요. "
        f"{outfit} {items}"
    )

def get_current_briefing(weather_data):
    import arrow

    temp = weather_data.get("temp")
    sky = weather_data.get("sky")
    rain = weather_data.get("rain")
    location = weather_data.get("location")

    try:
        outfit = recommend_outfit(
            temp_c=temp,
            tmx=temp,
            tmn=temp,
            month=arrow.now().month
        )
    except ValueError:
        outfit = "옷차림 정보를 불러올 수 없어요."

    items = recommend_items(
        sky=sky,
        rain=rain,
        pcp=weather_data.get("pcp", "강수없음"),
        wsd=weather_data.get("wsd", "0")
    )

    return (
        f"현재 {location} 날씨는 {sky}이고 {rain}이에요. "
        f"기온은 {temp}도예요. {outfit} {items}"
    )
