from fastapi import APIRouter

from app.schemas.user import ResumeRequest, UserCreate
from app.services.user_service import create_user, get_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/start")
def start_user(payload: UserCreate):
    user = create_user(
        user_name=payload.user_name,
        gender=payload.gender,
        age_group=payload.age_group,
        region=payload.region,
        consent=payload.consent,
    )
    return {
        "message": "사용자 정보가 저장되었습니다.",
        "user_id": user["user_id"],
        "resume_code": user["user_id"],
        "user": user,
    }


@router.post("/resume")
def resume_user(payload: ResumeRequest):
    user = get_user(payload.user_id)
    return {
        "message": "기존 기록을 불러왔습니다.",
        "user": user,
    }


@router.get("/{user_id}")
def get_user_info(user_id: str):
    return get_user(user_id)
