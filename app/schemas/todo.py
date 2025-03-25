from pydantic import BaseModel

class TodoText(BaseModel):
    text: str