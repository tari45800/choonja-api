# app/routers/parenting_report.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.parenting_report_service import get_parenting_report

router = APIRouter()

@router.get("/api/report")
def parenting_report(db: Session = Depends(get_db)):
    return get_parenting_report(db)
