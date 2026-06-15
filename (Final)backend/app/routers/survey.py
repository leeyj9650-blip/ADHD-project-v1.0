from fastapi import APIRouter

from app.schemas.survey import ReviewUpdate, SurveyAnswer
from app.services.survey_service import get_question, get_questions, get_user_answers, save_answer
from app.services.user_service import get_user, update_user_progress

router = APIRouter(prefix="/survey", tags=["survey"])


@router.get("/questions")
def list_questions():
    questions = get_questions()
    return {"total_count": len(questions), "questions": questions}


@router.get("/questions/{question_id}")
def read_question(question_id: int):
    return get_question(question_id)


@router.post("/answer")
def submit_answer(payload: SurveyAnswer):
    saved = save_answer(
        user_id=payload.user_id,
        question_id=payload.question_id,
        choice_id=payload.choice_id,
        voice_text=payload.voice_text,
        method=payload.method,
    )
    next_question_id = min(payload.question_id + 1, 20)
    update_user_progress(payload.user_id, next_question_id)
    return {"message": "응답이 저장되었습니다.", "answer": saved}


@router.get("/progress/{user_id}")
def get_progress(user_id: str):
    user = get_user(user_id)
    answers = get_user_answers(user_id)
    return {
        "user_id": user_id,
        "current_question_id": int(user["current_question_id"]),
        "status": user["status"],
        "response_count": len(answers),
        "answers": {str(k): v for k, v in answers.items()},
    }


@router.get("/review/{user_id}")
def get_review(user_id: str):
    answers = get_user_answers(user_id)
    questions = get_questions()
    review_items = []
    for q in questions:
        answer = answers.get(q["question_id"])
        review_items.append({
            "question_id": q["question_id"],
            "question": q["question"],
            "choices": q["choices"],
            "selected_choice_id": answer["choice_id"] if answer else None,
        })
    return {"items": review_items}


@router.post("/review/update")
def update_review_answer(payload: ReviewUpdate):
    saved = save_answer(payload.user_id, payload.question_id, payload.choice_id, None, "review")
    return {"message": "응답이 수정되었습니다.", "answer": saved}
