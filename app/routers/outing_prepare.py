from fastapi import APIRouter
from app.services.outing_prepare_service import get_outing_preparation_message

router = APIRouter()

@router.get("/api/outing/prepare")
async def get_outing_preparation():
    message = get_outing_preparation_message()
    return {
        "message": message
    }
