from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import HabitCreate, HabitUpdate, HabitResponse
from app.services import HabitService
from app.auth.dependencies import get_current_active_user


router = APIRouter()


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_data: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return HabitService.create_habit(
        db=db,
        user_id=current_user.id,
        habit_create=habit_data,
    )


@router.get("/", response_model=List[HabitResponse])
def get_habits(
    active_only: bool = Query(True),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    habits = HabitService.get_user_habits(
        db=db,
        user_id=current_user.id,
        active_only=active_only,
    )

    if search:
        search_lower = search.lower()
        habits = [
            habit for habit in habits
            if search_lower in habit.name.lower()
        ]

    return habits


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id)

    if not habit or habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: str,
    habit_data: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id)

    if not habit or habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return HabitService.update_habit(
        db=db,
        habit_id=habit_id,
        habit_update=habit_data,
    )


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id)

    if not habit or habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    HabitService.delete_habit(db=db, habit_id=habit_id)
    return None
  
