from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.event.crying import crying_event_service
from app.schemas.event import EventResponse

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/crying", response_model=EventResponse)
def handle_crying(db: Session = Depends(get_db)):
    return crying_event_service(db)
