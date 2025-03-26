from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.models.action import Action

def get_stock_count(
    db: Session,
    keyword_purchase: str,
    keyword_use: str,
    unit_per_purchase: int = 1
) -> int:
    # 구매 횟수
    purchase_count = (
        db.query(Schedule)
        .join(Action, Schedule.action_id == Action.id)
        .filter(Action.name == keyword_purchase)
        .count()
    )

    # 사용 횟수
    use_count = (
        db.query(Schedule)
        .join(Action, Schedule.action_id == Action.id)
        .filter(Action.name == keyword_use)
        .count()
    )

    stock = (purchase_count * unit_per_purchase) - use_count
    return max(stock, 0)
