from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class HabitResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
