from pydantic import BaseModel

class FixedMemoUpdate(BaseModel):
    schedule_id: int
    text: str
