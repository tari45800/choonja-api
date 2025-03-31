from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.d_day import DDayText, DDayResponse
from app.schemas.task import TaskText, TaskResponse
from app.services.d_day.create import create_d_day_service
from app.services.d_day.delete import delete_d_day_service  
from app.services.d_day import (
    create_d_day_service,
    delete_d_day_service,
)
router = APIRouter(prefix="/d-day", tags=["D-Day"])

@router.post("/", response_model=DDayResponse)
def create_d_day(body: DDayText, db: Session = Depends(get_db)):
    return create_d_day_service(body.text, db, include_after=body.include_after)

@router.delete("/", response_model=DDayResponse) 
def delete_d_day(body: TaskText, db: Session = Depends(get_db)):
    return delete_d_day_service(body.text, db)
