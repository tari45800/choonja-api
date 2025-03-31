from fastapi import FastAPI
from app.core.database import Base, engine
import uvicorn
from app.routers import task, fixed, d_day

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task.router)
app.include_router(fixed.router)
app.include_router(d_day.router)


@app.get("/")
def root():
    return {"message": "춘자 API 입니다"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
