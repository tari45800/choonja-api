from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import todo, schedule
import uvicorn

app = FastAPI()

# ✅ DB 테이블 자동 생성 (초기 1회만 호출됨)
Base.metadata.create_all(bind=engine)

# ✅ 라우터 연결
app.include_router(todo.router)
app.include_router(schedule.router)

@app.get("/")
def root():
    return {"message": "Welcome to Choonja API"}

# (선택) uvicorn 실행도 여기서 테스트 가능
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
