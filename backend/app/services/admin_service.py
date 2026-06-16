from collections import Counter
from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.constants import ADMIN_ID, ADMIN_PASSWORD, RESPONSES_CSV, RESULTS_CSV, USERS_CSV
from app.services.csv_service import ensure_csv_files, read_csv_rows


def verify_admin(admin_id: str, password: str) -> bool:
    return admin_id == ADMIN_ID and password == ADMIN_PASSWORD



def get_all_results() -> list[dict]:
    ensure_csv_files()
    return read_csv_rows(RESPONSES_CSV)



def get_stats() -> dict:
    rows = read_csv_rows(RESPONSES_CSV)
    gender_counter = Counter(row["Gender"] for row in rows if row.get("Gender"))
    age_counter = Counter(row["Age_group"] for row in rows if row.get("Age_group"))
    region_counter = Counter(row["Region"] for row in rows if row.get("Region"))
    return {
        "total_responses": len(rows),
        "by_gender": dict(gender_counter),
        "by_age_group": dict(age_counter),
        "by_region": dict(region_counter),
    }



def get_download_response(file_type: str):
    mapping: dict[str, Path] = {
        "users": USERS_CSV,
        "detail": RESULTS_CSV,
    }
    path = mapping.get(file_type)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="다운로드할 파일을 찾을 수 없습니다.")
    return FileResponse(path, filename=path.name, media_type="text/csv")
