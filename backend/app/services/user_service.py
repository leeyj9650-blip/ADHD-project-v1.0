from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.constants import USERS_CSV
from app.services.csv_service import USERS_HEADERS, ensure_csv_files, read_csv_rows, write_csv_rows


def create_user(user_name: str, gender: str, age_group: str, region: str, consent: bool) -> dict:
    ensure_csv_files()
    rows = read_csv_rows(USERS_CSV)
    now = datetime.now().isoformat()
    user_id = uuid4().hex[:12]
    new_row = {
        "user_id": user_id,
        "user_name": user_name,
        "gender": gender,
        "age_group": age_group,
        "region": region,
        "consent": str(consent),
        "created_at": now,
        "last_updated_at": now,
        "started_at": now,
        "completed_at": "",
        "current_question_id": "1",
        "status": "in_progress",
    }
    rows.append(new_row)
    write_csv_rows(USERS_CSV, USERS_HEADERS, rows)
    return new_row



def get_user(user_id: str) -> dict:
    ensure_csv_files()
    rows = read_csv_rows(USERS_CSV)
    for row in rows:
        if row["user_id"] == user_id:
            return row
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")



def update_user_progress(user_id: str, current_question_id: int, status: str = "in_progress", completed_at: str = "") -> dict:
    rows = read_csv_rows(USERS_CSV)
    found = None
    for row in rows:
        if row["user_id"] == user_id:
            row["current_question_id"] = str(current_question_id)
            row["status"] = status
            row["last_updated_at"] = datetime.now().isoformat()
            if completed_at:
                row["completed_at"] = completed_at
            found = row
            break
    if not found:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    write_csv_rows(USERS_CSV, USERS_HEADERS, rows)
    return found
