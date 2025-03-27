from pydantic import BaseModel

class TaskText(BaseModel):
    text: str