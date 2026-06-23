from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class CompletionCreate(BaseModel):
    completion_date: date
    notes: Optional[str] = None


class CompletionUpdate(BaseModel):
    notes: Optional[str] = None
    is_verified: Optional[bool] = None


class CompletionResponse(BaseModel):
    id: str
    habit_id: str
    completion_date: date
    completed_at: datetime
    notes: Optional[str] = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
