from app.constants import CHOICE_ID_TO_SCORE, HYPERACTIVE_IDS, INATTENTION_IDS


def get_score_from_choice(choice_id: int) -> int:
    return CHOICE_ID_TO_SCORE[choice_id]



def calculate_scores(answers: dict[int, int]) -> dict[str, int | str]:
    total_score = 0
    inattention_score = 0
    hyperactive_score = 0

    for question_id, choice_id in answers.items():
        score = get_score_from_choice(choice_id)
        total_score += score
        if question_id in INATTENTION_IDS:
            inattention_score += score
        elif question_id in HYPERACTIVE_IDS:
            hyperactive_score += score

    adhd_type = interpret_adhd_type(inattention_score, hyperactive_score)
    interpretation = interpret_total_score(total_score)

    return {
        "total_score": total_score,
        "inattention_score": inattention_score,
        "hyperactive_impulsive_score": hyperactive_score,
        "adhd_type": adhd_type,
        "interpretation": interpretation,
    }



def interpret_total_score(total_score: int) -> str:
    if total_score <= 19:
        return "ADHD 관련 어려움이 낮은 편으로 보입니다."
    if total_score <= 39:
        return "일부 ADHD 관련 경향이 관찰될 수 있습니다."
    if total_score <= 59:
        return "ADHD 관련 어려움이 다소 높은 편으로 보입니다."
    if total_score <= 79:
        return "ADHD 관련 경향이 비교적 높게 나타납니다."
    return "ADHD 관련 경향이 매우 높게 나타납니다. 전문가 상담을 권장합니다."



def interpret_adhd_type(inattention_score: int, hyperactive_score: int) -> str:
    if inattention_score >= 25 and hyperactive_score >= 25:
        return "복합형 경향"
    if inattention_score >= 25 and hyperactive_score < 25:
        return "부주의 우세 경향"
    if hyperactive_score >= 25 and inattention_score < 25:
        return "과잉행동/충동성 우세 경향"
    return "특정 우세 경향이 뚜렷하지 않음"
