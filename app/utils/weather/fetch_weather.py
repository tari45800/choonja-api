# app/utils/weather/fetch.py

import requests
import arrow
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
SERVICE_KEY = os.getenv("WEATHER_KEY")

SKY_STATUS = {"1": "맑음", "3": "구름 많음", "4": "흐림"}
PTY_STATUS = {"0": "비 안옴", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}

GRID_COORDS = {
   "부산 중구": (97, 74),
   "부산 서구": (97, 74),
   "부산 동구": (98, 75),
   "부산 영도구": (98, 74),
   "부산 부산진구": (98, 75),
   "부산 동래구": (99, 77),
   "부산 남구": (98, 75),
   "부산 북구": (97, 77),
   "부산 해운대구": (100, 76),
   "부산 사하구": (96, 74),
   "부산 금정구": (99, 78),
   "부산 강서구": (96, 76),
   "부산 연제구": (99, 76),
   "부산 수영구": (99, 76),
   "부산 사상구": (97, 75),
}

def get_grid_coords(location: str):
    return GRID_COORDS.get(location, (98, 76))

def fetch_weather_items(location="부산 수영구"):
    nx, ny = get_grid_coords(location)
    now = arrow.now("Asia/Seoul")
    base_date = now.format("YYYYMMDD")
    base_time = "0200"

    params = {
        "serviceKey": SERVICE_KEY,
        "dataType": "JSON",
        "pageNo": "1",
        "numOfRows": "1000",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    res = requests.get(API_URL, params=params)
    print("📦 응답 상태 코드:", res.status_code)

    if "application/json" not in res.headers.get("Content-Type", ""):
        print("❌ 응답이 JSON이 아님")
        print("📦 응답 본문:\n", res.text)
        return []

    try:
        return res.json()['response']['body']['items']['item']
    except Exception as e:
        print("❌ JSON 파싱 에러:", e)
        return []
