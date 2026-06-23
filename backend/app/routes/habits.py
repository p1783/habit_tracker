from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.exceptions import HabitNotFound
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from app.services.habit_service import HabitService

router = APIRouter(prefix="/api/habits", tags=["habits"])


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_data: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HabitService.create_habit(db, current_user.id, habit_data)


@router.get("", response_model=list[HabitResponse])
def get_habits(
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HabitService.get_user_habits(db, current_user.id, is_active)


@router.get("/search", response_model=list[HabitResponse])
def search_habits(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HabitService.search_habits(db, current_user.id, query)


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)

    if not habit:
        raise HabitNotFound()

    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: str,
    habit_data: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)

    if not habit:
        raise HabitNotFound()

    return HabitService.update_habit(db, habit, habit_data)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)

    if not habit:
        raise HabitNotFound()

    HabitService.delete_habit(db, habit)
    return None