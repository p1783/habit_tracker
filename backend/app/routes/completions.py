from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import CompletionCreate, CompletionResponse
from app.services import HabitService, CompletionService
from app.auth.dependencies import get_current_active_user


router = APIRouter()


@router.post(
    "/habits/{habit_id}",
    response_model=CompletionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_completion(
    habit_id: str,
    completion_data: CompletionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id)

    if not habit or habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return CompletionService.create_completion(
        db=db,
        habit_id=habit_id,
        completion_create=completion_data,
    )


@router.get("/habits/{habit_id}", response_model=List[CompletionResponse])
def get_habit_completions(
    habit_id: str,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id)

    if not habit or habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return CompletionService.get_habit_completions(
        db=db,
        habit_id=habit_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/habits/{habit_id}/today")
def is_habit_completed_today(
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

    return {
        "habit_id": habit_id,
        "completed_today": CompletionService.is_habit_completed_today(db, habit_id),
    }


@router.delete("/{completion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_completion(
    completion_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    completion = CompletionService.get_completion_by_id(db, completion_id)

    if not completion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completion not found",
        )

    habit = HabitService.get_habit_by_id(db, completion.habit_id)

    if not habit or habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completion not found",
        )

    CompletionService.delete_completion(db=db, completion_id=completion_id)
    return None
  
