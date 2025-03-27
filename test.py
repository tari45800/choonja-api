from app.services.weather.weather_data import get_today_forecast, get_current_weather
from app.services.weather.weather_recommendation import get_weather_briefing, get_current_briefing


today = get_today_forecast("부산 수영구")
current = get_current_weather("부산 수영구")

print("🗓️ 아침 Siri 브리핑:")
print(get_weather_briefing(today))

print("\n⏰ 외출 전 현재 날씨 브리핑:")
print(get_current_briefing(current))