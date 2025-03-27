from fastapi import FastAPI
from app.core.database import Base, engine
import uvicorn
from app.routers import task

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task.router)


@app.get("/")
def root():
    return {"message": "Welcome to Choonja API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
