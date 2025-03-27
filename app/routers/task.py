from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.task import create_task_service
from app.schemas.task import TaskText

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=dict)
def create_task(body: TaskText, db: Session = Depends(get_db)):
    return create_task_service(body.text, db)

