from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TodoText
from app.services.schedule_service import register_schedule
from app.core.database import get_db

router = APIRouter()

@router.post("/api/schedule")
def parse_and_register_schedule(item: TodoText, db: Session = Depends(get_db)):
    return register_schedule(db, item.text)
