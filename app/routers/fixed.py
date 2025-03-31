from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskText, TaskResponse
from app.schemas.fixed import FixedMemoUpdate
from app.services.fixed import (
    create_fixed_service,
    update_fixed_service,
    update_latest_fixed_service,
    delete_latest_fixed_service,
    update_fixed_memo_service,
)

router = APIRouter(prefix="/fixed", tags=["Fixed"])

# 일정 등록
@router.post("/", response_model=TaskResponse)
def create_fixed(body: TaskText, db: Session = Depends(get_db)):
    return create_fixed_service(body.text, db)

# 오늘 고정 일정 수정
@router.put("/", response_model=TaskResponse)
def update_fixed(body: TaskText, db: Session = Depends(get_db)):
    return update_fixed_service(body.text, db)

# 최근 고정 일정 수정
@router.put("/latest", response_model=TaskResponse)
def update_latest_fixed(body: TaskText, db: Session = Depends(get_db)):
    return update_latest_fixed_service(body.text, db)

# 메모 추가
@router.put("/memo", response_model=TaskResponse)
def update_fixed_memo(body: FixedMemoUpdate, db: Session = Depends(get_db)):
    return update_fixed_memo_service(body.schedule_id, body.text, db)

# 최근 고정 일정 삭제
@router.delete("/", response_model=TaskResponse)
def delete_fixed(body: TaskText, db: Session = Depends(get_db)):
    return delete_latest_fixed_service(body.text, db)
