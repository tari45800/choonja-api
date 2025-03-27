from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.schedule import Schedule
from app.models.action import Action

def get_weekly_event_counts(db: Session) -> dict:
    seven_days_ago = datetime.now() - timedelta(days=7)

    keywords = {
        "feeding": "수유 시작",
        "sleep": "애기 수면 시작",
        "diaper": "기저귀 교체"
    }

    results = {}

    for key, action_name in keywords.items():
        count = (
            db.query(Schedule)
            .join(Action, Schedule.action_id == Action.id)
            .filter(
                Action.name == action_name,
                Schedule.created_at >= seven_days_ago
            )
            .count()
        )
        results[key] = count

    return results
