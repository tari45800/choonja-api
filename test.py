import requests
import datetime
import threading

# 👉 여기에 오늘 할일 예시 데이터
schedules = [
    {"name": "기저귀 갈기", "year": "2025", "month": "3", "day": "25", "time": "17:36"},
    {"name": "수유하기", "year": "2025", "month": "3", "day": "25", "time": "17:36"},
    {"name": "산책가기", "year": "2025", "month": "3", "day": "26", "time": "10:00"},
]

webhook_url = "http://localhost:8123/api/webhook/choonja_home_assistant"

def send_notification(schedule):
    message = f"🍼 {schedule['name']} 할 시간이야!"
    data = {"message": message}
    res = requests.post(webhook_url, json=data)
    print(f"[{datetime.datetime.now().time()}] ⏰ 알림 보냄: {message} (Status: {res.status_code})")

def schedule_task(schedule):
    now = datetime.datetime.now()
    task_time = datetime.datetime(
        year=int(schedule["year"]),
        month=int(schedule["month"]),
        day=int(schedule["day"]),
        hour=int(schedule["time"].split(":")[0]),
        minute=int(schedule["time"].split(":")[1])
    )
    delay = (task_time - now).total_seconds()

    if delay > 0:
        print(f"⏳ '{schedule['name']}' 알림 예약됨 → {schedule['time']}")
        threading.Timer(delay, send_notification, [schedule]).start()
    else:
        print(f"❌ '{schedule['name']}'은(는) 이미 지난 시간임")

def main():
    today = datetime.date.today()
    for schedule in schedules:
        if (int(schedule["year"]) == today.year and
            int(schedule["month"]) == today.month and
            int(schedule["day"]) == today.day):
            schedule_task(schedule)

if __name__ == "__main__":
    main()
