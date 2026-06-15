from fastapi import APIRouter

router = APIRouter(prefix="/home", tags=["home"])


@router.get("/")
def read_home():
    return {
        "title": "ADHD 자가진단 ❤️",
        "message": "ADHD 자가진단 API 서버가 실행 중입니다.",
    }
