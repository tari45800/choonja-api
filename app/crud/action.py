from sqlalchemy.orm import Session
from app.models.action import Action
from datetime import datetime

# 액션 찾기
def find_action(name: str, db: Session):
    action = db.query(Action).filter(Action.name == name).first()
    if action:
        return {
            "result": action,
            "message": f"'{name}' 액션을 찾았습니다."
        }
    else:
        return {
            "result": None,
            "message": f"'{name}' 액션을 찾을 수 없습니다."
        }

# 액션 만들기
def create_action(name: str, category: str, db: Session, duration_min: int = None, parent_id: int = None):
    existing_check = find_action(name, db)

    if existing_check["result"]:
        return {
            "result": existing_check["result"],
            "message": f"'{name}'은 이미 존재하는 액션입니다"
        }

    action = Action(
        name=name,
        category=category,
        duration_min=duration_min,
        parent_id=parent_id,
        created_at=datetime.utcnow()
    )
    db.add(action)
    db.commit()
    db.refresh(action)

    return {
        "result": action,
        "message": f"'{name}' 액션이 새로 등록 되었습니다"
    }
