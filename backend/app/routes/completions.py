from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.user import User
from app.models.habit_completion import HabitCompletion
from app.schemas.habit_completion import HabitCompletionCreate, HabitCompletionResponse
from app.services.habit_service import HabitService
from app.services.habit_completion_service import HabitCompletionService
from app.auth.security import get_current_user
from app.exceptions import HabitNotFound, CompletionAlreadyExists

router = APIRouter(prefix="/api/habits", tags=["completions"])


@router.post("/{habit_id}/completions", response_model=HabitCompletionResponse, status_code=status.HTTP_201_CREATED)
def create_completion(
    habit_id: str,
    completion_data: HabitCompletionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a habit as completed for a specific date
    
    Args:
        habit_id: ID of the habit
        completion_data: Completion date and optional notes
    
    Returns:
        HabitCompletionResponse: Created completion record
    
    Raises:
        404: Habit not found
        400: Habit already completed on this date
    """
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    
    # Check if already completed on this date
    existing = HabitCompletionService.get_completion_by_date(
        db, habit_id, completion_data.completion_date
    )
    if existing:
        raise CompletionAlreadyExists()
    
    completion = HabitCompletionService.create_completion(
        db, habit_id, completion_data
    )
    return completion


@router.get("/{habit_id}/completions", response_model=list[HabitCompletionResponse])
def get_completions(
    habit_id: str,
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get completions for a habit with optional date range filtering
    
    Args:
        habit_id: ID of the habit
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering
    
    Returns:
        list[HabitCompletionResponse]: List of completions
    
    Raises:
        404: Habit not found
    """
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    
    if start_date and end_date:
        completions = HabitCompletionService.get_completions_by_date_range(
            db, habit_id, start_date, end_date
        )
    else:
        completions = HabitCompletionService.get_completions_by_habit(db, habit_id)
    
    return completions


@router.delete("/{habit_id}/completions/{completion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_completion(
    habit_id: str,
    completion_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a habit completion record
    
    Args:
        habit_id: ID of the habit
        completion_id: ID of the completion to delete
    
    Raises:
        404: Habit or completion not found
    """
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    
    completion = db.query(HabitCompletion).filter(
        HabitCompletion.id == completion_id,
        HabitCompletion.habit_id == habit_id,
    ).first()
    
    if not completion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completion not found",
        )
    
    HabitCompletionService.delete_completion(db, completion)
    return None
