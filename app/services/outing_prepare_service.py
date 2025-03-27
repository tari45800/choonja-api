from app.services.weather.weather_recommendation import get_current_briefing 
from app.services.weather.weather_data import get_current_weather 

def get_outing_preparation_message(region: str = "부산 수영구"):
    weather_data = get_current_weather(region) 
    weather = get_current_briefing(weather_data) 

    items = ["핸드폰", "카드", "차키"]
    item_sentence = ", ".join(items[:-1]) + f", {items[-1]}" if len(items) > 1 else items[0]

    message = (
        f"{weather}"
        f"그리고 외출 시 {item_sentence}를 챙기세요."
    )

    return message