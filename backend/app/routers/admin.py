from fastapi import APIRouter, HTTPException

from app.schemas.admin import AdminLogin
from app.services.admin_service import get_all_results, get_download_response, get_stats, verify_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login")
def login(payload: AdminLogin):
    if not verify_admin(payload.admin_id, payload.password):
        raise HTTPException(status_code=401, detail="관리자 인증에 실패했습니다.")
    return {"message": "관리자 로그인 성공"}


@router.get("/results")
def results():
    data = get_all_results()
    return {"count": len(data), "data": data}


@router.get("/stats")
def stats():
    return get_stats()


@router.get("/download/{file_type}")
def download(file_type: str):
    return get_download_response(file_type)
