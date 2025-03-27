from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TodoText
from app.core.database import get_db
from app.services.todo_service import register_todo

router = APIRouter()


@router.post("/api/todo")
def parse_and_register_todo(item: TodoText, db: Session = Depends(get_db)):
    return register_todo(db, item.text)
