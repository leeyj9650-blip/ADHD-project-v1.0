import csv
import json
from pathlib import Path
from typing import Dict, List

from app.constants import DATA_DIR, RESULTS_CSV, RESPONSES_CSV, USERS_CSV


USERS_HEADERS = [
    "user_id", "user_name", "gender", "age_group", "region", "consent",
    "created_at", "last_updated_at", "started_at", "completed_at",
    "current_question_id", "status"
]

RESPONSES_HEADERS = [
    "Data_time", "Return_time", "User_id", "User_name", "Gender", "Age_group", "Region",
    "총점", "부주의 점수", "과잉행동/충동성 점수", "ADHD 유형", "해석 문구",
    "Duration_seconds", "Response_count"
]

RESULTS_HEADERS = [
    "Data_time", "Return_time", "User_id", "User_name", "Gender", "Age_group", "Region",
    *[f"Q{i}" for i in range(1, 21)], "총점", "부주의 점수", "과잉행동/충동성 점수", "ADHD 유형", "해석 문구"
]

# 초기 파일 생성
def ensure_csv_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_file(USERS_CSV, USERS_HEADERS)
    _ensure_file(RESPONSES_CSV, RESPONSES_HEADERS)
    _ensure_file(RESULTS_CSV, RESULTS_HEADERS)



def _ensure_file(path: Path, headers: List[str]) -> None:
    if not path.exists():
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


# 읽기
def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# 전체 수정
def write_csv_rows(path: Path, headers: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


# 한 줄 추가
def append_csv_row(path: Path, headers: List[str], row: Dict[str, str]) -> None:
    with path.open("a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(row)

# 파일 생성
def ensure_json_file(path: Path, default: dict | list) -> None:
    if not path.exists():
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")

# 읽기
def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

# 저장
def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
