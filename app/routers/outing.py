from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.todo import TodoText
from app.services.outing_schedule_service import register_outing_schedule
from app.core.database import get_db

router = APIRouter()

@router.post("/api/schedule/outing")
def parse_and_register_outing_schedule(item: TodoText, db: Session = Depends(get_db)):
    return register_outing_schedule(db, item.text)
