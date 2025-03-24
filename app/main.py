from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import *  # __init__.py 덕에 전체 모델 인식됨

# ⛏️ 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "춘자 백엔드 살아있습니다 🧼"}
