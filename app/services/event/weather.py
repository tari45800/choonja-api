from app.utils.weather.fetch_weather import fetch_weather_items
from app.utils.weather.parse_weather import parse_items_to_current_weather
from app.utils.weather.describe import get_today_tmp_pcp_list
from app.utils.weather.weather_message import generate_weather_message

def weather_event_service(location: str = "부산 수영구"):
    """
    날씨 이벤트 발생 시 가공된 날씨 메시지까지 출력해보는 서비스
    """
    items = fetch_weather_items("부산 수영구")
    if not items:
        return {"message": f"{location} 날씨 데이터를 불러오지 못했어요."}

    # 날씨 JSON 가공
    weather_data = parse_items_to_current_weather(items, location="부산 수영구")

    # TMP 리스트 가져오기 (시간대별 분석용)
    tmp_list, _ = get_today_tmp_pcp_list(items)

    # 자연어 메시지 생성 (기온 흐름 포함)
    weather_message = generate_weather_message(weather_data, tmp_list)

    print("🗣️ 날씨 메시지:", weather_message)

    return {
        "message": weather_message,
        "weather": weather_data
    }
