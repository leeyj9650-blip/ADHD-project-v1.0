from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=50)
    gender: str
    age_group: str
    region: str
    consent: bool = True


class ResumeRequest(BaseModel):
    user_id: str


class UserProfile(BaseModel):
    user_id: str
    user_name: str
    gender: str
    age_group: str
    region: str
    consent: bool
    created_at: datetime
    last_updated_at: datetime
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_question_id: int = 1
    status: str = "in_progress"
