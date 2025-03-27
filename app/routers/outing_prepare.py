from fastapi import APIRouter

router = APIRouter()

@router.get("/outing/prepare")
async def get_outing_preparation():
    return {
        "message": "외출 준비 정보 호출 성공! (임시 라우터)"
    }
