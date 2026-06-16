from fastapi import APIRouter

from app.schemas.result import ResultResponse
from app.services.result_service import finalize_result, get_latest_result

router = APIRouter(prefix="/result", tags=["result"])


@router.post("/finalize/{user_id}", response_model=ResultResponse)
def finalize(user_id: str):
    return finalize_result(user_id)


@router.get("/latest/{user_id}")
def latest_result(user_id: str):
    return get_latest_result(user_id)
