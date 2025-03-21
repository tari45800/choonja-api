# app/main.py

from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import actions  # 앞으로 만들 라우터

# DB 테이블 자동 생성 (초기 개발용)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="춘자 API 🧼",
    description="육아 자동화 시스템 백엔드",
    version="0.1.0"
)

# 라우터 등록
app.include_router(actions.router, prefix="/actions", tags=["액션"])

# 헬스 체크용 루트
@app.get("/")
def read_root():
    return {"message": "여기는 춘자입니다 🧺 오늘도 자동으로 도와드릴게요!"}
