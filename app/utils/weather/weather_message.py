from app.utils.weather.describe import (
    get_rain_strength,
    get_wind_strength,
)

from app.utils.weather.temp_message import (
    generate_timeblock_temp_briefing,
    generate_temp_feeling_sentence,
)
import arrow

def generate_weather_message(weather_data: dict, tmp_list: list = None) -> str:
    try:
        location = weather_data.get("location", "지역 정보 없음")
        temp = weather_data.get("temp", "?")
        highest = weather_data.get("highest", "?")
        lowest = weather_data.get("lowest", "?")
        sky = weather_data.get("sky", "날씨 정보 없음")
        rain = weather_data.get("rain", "비 여부 알 수 없음")
        pcp_raw = weather_data.get("pcp", "0").replace("mm", "").strip()
        wsd_raw = weather_data.get("wsd", "0").strip()

        # 숫자 변환
        try:
            pcp_val = float(pcp_raw) if pcp_raw not in ["강수없음", ""] else 0
        except:
            pcp_val = 0
        try:
            wsd_val = float(wsd_raw)
        except:
            wsd_val = 0

        # 기본 날씨 설명
        rain_desc = get_rain_strength(pcp_val)
        wind_desc = get_wind_strength(wsd_val)

        base_message = (
            f"{location}의 현재 날씨는 {sky}이고 {rain} 상태입니다. "
            f"기온은 {temp}도이며, 오늘 최고 {highest}도, 최저 {lowest}도입니다. "
            f"{rain_desc} {wind_desc}"
        )

        # 추가: 하루 기온 흐름 (선택적)
        if tmp_list:
            now = arrow.now("Asia/Seoul")
            hour = now.hour
            month = now.month
            temp_blocks = generate_timeblock_temp_briefing(tmp_list, hour, month)
            temp_message = generate_temp_feeling_sentence(temp_blocks)
            return base_message + " " + temp_message

        return base_message

    except Exception:
        return "날씨 메시지를 생성하는 데 문제가 생겼어요."
