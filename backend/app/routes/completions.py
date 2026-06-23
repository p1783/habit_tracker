from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.exceptions import CompletionAlreadyExists, HabitNotFound
from app.models.completion import Completion
from app.models.user import User
from app.schemas.completion import CompletionCreate, CompletionResponse
from app.services.completion_service import CompletionService
from app.services.habit_service import HabitService

router = APIRouter(prefix="/api/habits", tags=["completions"])


@router.post(
    "/{habit_id}/completions",
    response_model=CompletionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_completion(
    habit_id: str,
    completion_data: CompletionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)

    if not habit:
        raise HabitNotFound()

    existing = CompletionService.get_completion_by_date(
        db,
        habit_id,
        completion_data.completion_date,
    )

    if existing:
        raise CompletionAlreadyExists()

    return CompletionService.create_completion(db, habit_id, completion_data)


@router.get("/{habit_id}/completions", response_model=list[CompletionResponse])
def get_completions(
    habit_id: str,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)

    if not habit:
        raise HabitNotFound()

    if start_date and end_date:
        return CompletionService.get_completions_by_date_range(
            db,
            habit_id,
            start_date,
            end_date,
        )

    return CompletionService.get_completions_by_habit(db, habit_id)


@router.delete(
    "/{habit_id}/completions/{completion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_completion(
    habit_id: str,
    completion_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)

    if not habit:
        raise HabitNotFound()

    completion = (
        db.query(Completion)
        .filter(
            Completion.id == completion_id,
            Completion.habit_id == habit_id,
        )
        .first()
    )

    if not completion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completion not found",
        )

    CompletionService.delete_completion(db, completion)
    return None