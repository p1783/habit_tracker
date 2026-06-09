from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class CompletionCreate(BaseModel):
    completion_date: date
    notes: Optional[str] = None

class CompletionResponse(BaseModel):
    id: str
    habit_id: str
    completion_date: date
    completed_at: datetime
    notes: Optional[str]
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
