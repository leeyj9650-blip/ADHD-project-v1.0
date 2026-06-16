from fastapi import HTTPException

from app.constants import CHOICES, DRAFTS_JSON
from app.questions import QUESTIONS
from app.services.csv_service import ensure_csv_files, ensure_json_file, read_json, write_json


def _load_all_answers() -> dict:
    ensure_csv_files()
    ensure_json_file(DRAFTS_JSON, {})
    return read_json(DRAFTS_JSON, {})


def _write_all_answers(data: dict) -> None:
    write_json(DRAFTS_JSON, data)


def get_questions():
    return [{**q, "choices": CHOICES} for q in QUESTIONS]


def get_question(question_id: int):
    for question in QUESTIONS:
        if question["question_id"] == question_id:
            return {**question, "choices": CHOICES}
    raise HTTPException(status_code=404, detail="문항을 찾을 수 없습니다.")


def save_answer(user_id: str, question_id: int, choice_id: int, voice_text: str | None, method: str) -> dict:
    if choice_id not in {0, 1, 2, 3}:
        raise HTTPException(status_code=400, detail="유효하지 않은 choice_id 입니다.")
    all_answers = _load_all_answers()
    user_answers = all_answers.setdefault(user_id, {})
    user_answers[str(question_id)] = {
        "question_id": question_id,
        "choice_id": choice_id,
        "voice_text": voice_text or "",
        "method": method,
    }
    _write_all_answers(all_answers)
    return user_answers[str(question_id)]


def get_user_answers(user_id: str) -> dict[int, dict]:
    all_answers = _load_all_answers()
    answers = all_answers.get(user_id, {})
    return {int(k): v for k, v in answers.items()}


def clear_user_answers(user_id: str) -> None:
    all_answers = _load_all_answers()
    all_answers.pop(user_id, None)
    _write_all_answers(all_answers)
