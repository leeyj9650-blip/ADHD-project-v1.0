from typing import Optional
from pydantic import BaseModel, Field


class SurveyAnswer(BaseModel):
    user_id: str
    question_id: int = Field(..., ge=1, le=20)
    choice_id: int = Field(..., ge=0, le=3)
    voice_text: Optional[str] = None
    method: str = "manual"


class ReviewUpdate(BaseModel):
    user_id: str
    question_id: int = Field(..., ge=1, le=20)
    choice_id: int = Field(..., ge=0, le=3)
