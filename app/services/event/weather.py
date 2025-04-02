from app.utils.weather.fetch_weather import fetch_weather_items
from app.utils.weather.parse_weather import parse_items_to_current_weather
from app.utils.weather.describe import get_today_tmp_pcp_list
from app.utils.weather.weather_message import generate_weather_message

def weather_event_service(location):
    
    location = "부산 수영구"

    items = fetch_weather_items(location)
    if not items:
        return {"message": f"{location} 날씨 데이터를 불러오지 못했어요."}

    # 날씨 JSON 가공
    weather_data = parse_items_to_current_weather(items, location=location)

    # TMP, PCP 리스트 가져오기
    tmp_list, pcp_list = get_today_tmp_pcp_list(items)

    # 자연어 메시지 생성 (기온 + 강수 흐름 포함)
    weather_message = generate_weather_message(weather_data, tmp_list, pcp_list)

    print("🗣️ 날씨 메시지:", weather_message)

    return {
        "message": weather_message,
        "weather": weather_data
    }
