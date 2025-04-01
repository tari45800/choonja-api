from pydantic import BaseModel

class EventResponse(BaseModel):
    message: str
