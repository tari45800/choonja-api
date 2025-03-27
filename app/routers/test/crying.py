from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.crying_service import handle_crying_event_service

router = APIRouter()

@router.get("/api/event/crying")
def handle_crying_event(db: Session = Depends(get_db)):
    return handle_crying_event_service(db)
