from datetime import datetime
from typing import Dict
from pydantic import BaseModel


class ResultResponse(BaseModel):
    user_id: str
    user_name: str
    started_at: datetime
    finished_at: datetime
    duration_seconds: int
    response_count: int
    answers: Dict[str, int]
    total_score: int
    inattention_score: int
    hyperactive_impulsive_score: int
    adhd_type: str
    interpretation: str
