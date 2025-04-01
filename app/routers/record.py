from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.record import RecordText, RecordResponse
from app.services.record import create_record_service

router = APIRouter(prefix="/records", tags=["Records"])

# 기록 등록
@router.post("/", response_model=RecordResponse)
def create_record(body: RecordText, db: Session = Depends(get_db)):
    return create_record_service(body.text, db)
