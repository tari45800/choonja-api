from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TodoText
from app.services.record_service import register_record
from app.core.database import get_db

router = APIRouter()

@router.post("/api/record")
def parse_and_register_record(item: TodoText, db: Session = Depends(get_db)):
    return register_record(db, item.text)
