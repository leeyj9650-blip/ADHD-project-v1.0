from datetime import datetime
from fastapi import HTTPException

from app.constants import RESPONSES_CSV, RESULTS_CSV
from app.services.csv_service import (
    RESPONSES_HEADERS,
    RESULTS_HEADERS,
    append_csv_row,
    ensure_csv_files,
    read_csv_rows,
)
from app.services.score_service import calculate_scores
from app.services.survey_service import clear_user_answers, get_user_answers
from app.services.user_service import get_user, update_user_progress


def finalize_result(user_id: str) -> dict:
    ensure_csv_files()
    user = get_user(user_id)
    answers_dict = get_user_answers(user_id)
    if len(answers_dict) < 20:
        raise HTTPException(status_code=400, detail="20문항 응답이 완료되지 않았습니다.")

    normalized_answers = {question_id: item["choice_id"] for question_id, item in answers_dict.items()}
    scores = calculate_scores(normalized_answers)

    started_at = datetime.fromisoformat(user["started_at"])
    finished_at = datetime.now()
    duration_seconds = int((finished_at - started_at).total_seconds())
    response_count = len(normalized_answers)

    summary_row = {
        "Data_time": user["started_at"],
        "Return_time": finished_at.isoformat(),
        "User_id": user_id,
        "User_name": user["user_name"],
        "Gender": user["gender"],
        "Age_group": user["age_group"],
        "Region": user["region"],
        "총점": str(scores["total_score"]),
        "부주의 점수": str(scores["inattention_score"]),
        "과잉행동/충동성 점수": str(scores["hyperactive_impulsive_score"]),
        "ADHD 유형": scores["adhd_type"],
        "해석 문구": scores["interpretation"],
        "Duration_seconds": str(duration_seconds),
        "Response_count": str(response_count),
    }
    append_csv_row(RESPONSES_CSV, RESPONSES_HEADERS, summary_row)

    detail_row = {
        "Data_time": user["started_at"],
        "Return_time": finished_at.isoformat(),
        "User_id": user_id,
        "User_name": user["user_name"],
        "Gender": user["gender"],
        "Age_group": user["age_group"],
        "Region": user["region"],
        **{f"Q{i}": str(normalized_answers.get(i, "")) for i in range(1, 21)},
        "총점": str(scores["total_score"]),
        "부주의 점수": str(scores["inattention_score"]),
        "과잉행동/충동성 점수": str(scores["hyperactive_impulsive_score"]),
        "ADHD 유형": scores["adhd_type"],
        "해석 문구": scores["interpretation"],
    }
    append_csv_row(RESULTS_CSV, RESULTS_HEADERS, detail_row)

    update_user_progress(user_id, 20, status="completed", completed_at=finished_at.isoformat())
    clear_user_answers(user_id)

    return {
        "user_id": user_id,
        "user_name": user["user_name"],
        "started_at": user["started_at"],
        "finished_at": finished_at.isoformat(),
        "duration_seconds": duration_seconds,
        "response_count": response_count,
        "answers": {f"Q{i}": normalized_answers.get(i) for i in range(1, 21)},
        **scores,
    }



def get_latest_result(user_id: str) -> dict:
    rows = read_csv_rows(RESPONSES_CSV)
    matched = [row for row in rows if row["User_id"] == user_id]
    if not matched:
        raise HTTPException(status_code=404, detail="결과를 찾을 수 없습니다.")
    return matched[-1]
