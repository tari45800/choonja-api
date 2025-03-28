from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskText, TaskResponse
from app.services.task import (
    create_task_service,
    update_task_service,
    # delete_task_service
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(body: TaskText, db: Session = Depends(get_db)):
    return create_task_service(body.text, db)

@router.put("/", response_model=TaskResponse)
def update_task(body: TaskText, db: Session = Depends(get_db)):
    return update_task_service(body.text, db)

# @router.delete("/", response_model=TaskResponse)
# def delete_task(body: TaskText, db: Session = Depends(get_db)):
#     return delete_task_service(body.text, db)
