from sqlalchemy.orm import Session
from datetime import timedelta, date
from app.utils.parser.extract_parts import extract_parts
from app.crud.action import create_action
from app.crud.schedule import create_schedule

# 과거 알림 (기준일 이전)
D_DAY_BEFORE = {
    "하루 전": 1,
    "3일 전": 3,
    "일주일 전": 7,
    "한 달 전": 30,
    "세 달 전": 90,
}

# 미래 알림 (기준일 이후)
D_DAY_AFTER = {
    "일주일 후": 7,
    "한 달 후": 30,
    "100일 후": 100,
    "1년 후": 365,
    "2년 후": 365 * 2,
    "3년 후": 365 * 3,
    "4년 후": 365 * 4,
    "5년 후": 365 * 5,
    "10년 후": 365 * 10,
    "50년 후": 365 * 50,
    "100년 후": 365 * 100,
}

def create_d_day_service(text: str, db: Session, include_after: bool = False):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed

    dt = parsed['dt']
    an = parsed['action']

    if not dt:
        return {
            "result": None,
            "message": "디데이 날짜를 인식할 수 없습니다."
        }

    if not an:
        return {
            "result": None,
            "message": "디데이 일정 이름을 인식할 수 없습니다."
        }

    action_name = f"{an} 디데이"
    action_res = create_action(name=action_name, category="d_day", db=db)
    action = action_res["result"]

    # 기준일 등록
    base_schedule = create_schedule(
        action_id=action.id,
        year=dt.year,
        month=str(dt.month),
        day=str(dt.day),
        memo="당일",
        db=db
    )

    today = date.today()
    alert_labels = []

    # 과거 알림 일정 등록
    for label, offset in D_DAY_BEFORE.items():
        dday_date = dt.date() - timedelta(days=offset)
        if dday_date < today:
            continue  # 과거 일정은 스킵
        create_schedule(
            action_id=action.id,
            year=dday_date.year,
            month=str(dday_date.month),
            day=str(dday_date.day),
            memo=label,
            db=db
        )
        alert_labels.append(label)

    # ➕ 이후 알림 일정 등록
    if include_after:
        for label, offset in D_DAY_AFTER.items():
            dday_date = dt.date() + timedelta(days=offset)
            create_schedule(
                action_id=action.id,
                year=dday_date.year,
                month=str(dday_date.month),
                day=str(dday_date.day),
                memo=label,
                db=db
            )
            alert_labels.append(label)

    return {
        "result": base_schedule["result"],
        "message": f"'{action_name}' 일정이 {dt.year}-{dt.month:02}-{dt.day:02}에 등록되었고, "
                   f"{', '.join(alert_labels)} 반복 알림도 등록되었습니다."
    }
