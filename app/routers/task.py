from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskText, TaskResponse
from app.services.task import (
    create_task_service,
    update_task_service,
    update_latest_task_service,
    delete_latest_task_service,
    update_schedule_done_service
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# 할 일 등록
@router.post("/", response_model=TaskResponse)
def create_task(body: TaskText, db: Session = Depends(get_db)):
    return create_task_service(body.text, db)

# 오늘 할 일 날짜 수정
@router.put("/", response_model=TaskResponse)
def update_task(body: TaskText, db: Session = Depends(get_db)):
    return update_task_service(body.text, db)

# 최근 할 일 날짜, 이름 수정
@router.put("/latest", response_model=TaskResponse)
def update_latest_task(body: TaskText, db: Session = Depends(get_db)):
    return update_latest_task_service(body.text, db)

# 할 일 완료
@router.put("/done", response_model=TaskResponse)
def update_task_done(body: TaskText, db: Session = Depends(get_db)):
    return update_schedule_done_service(body.text, db)

# 최근 할 일 삭제
@router.delete("/", response_model=TaskResponse)
def delete_task(body: TaskText, db: Session = Depends(get_db)):
    return delete_latest_task_service(body.text, db)

