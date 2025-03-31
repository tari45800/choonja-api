from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.record import RecordText
from app.services.record.create import create_record_service

router = APIRouter(prefix="/records", tags=["Records"])

@router.post("/")
async def create_record(body: RecordText, request: Request, db: Session = Depends(get_db)):
    return create_record_service(body.text, db)
