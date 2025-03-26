from sqlalchemy.orm import Session
from app.models.action import Action

def get_or_create_action(db: Session, name: str, category: str = "task") -> Action:
    action = db.query(Action).filter(
        Action.name == name
    ).first()
    
    if action:
        return action

    new_action = Action(
        name=name,
        category=category,
        parent_id=None,
        duration_min=None,
        briefing_key=None,
        is_alarm_enabled=None,
        is_voice_enabled=None,
        is_push_enabled=None
    )
    db.add(new_action)
    db.commit()
    db.refresh(new_action)
    return new_action
