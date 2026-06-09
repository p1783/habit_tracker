from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.services.habit_service import HabitService
from app.auth.security import get_current_user
from app.exceptions import HabitNotFound, PermissionDenied

router = APIRouter(prefix="/api/habits", tags=["habits"])


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_data: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new habit for the current user"""
    habit = HabitService.create_habit(db, current_user.id, habit_data)
    return habit


@router.get("", response_model=list[HabitResponse])
def get_habits(
    is_active: bool = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all habits for current user with optional filtering"""
    habits = HabitService.get_user_habits(db, current_user.id, is_active)
    return habits


@router.get("/search", response_model=list[HabitResponse])
def search_habits(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search habits by name"""
    habits = HabitService.search_habits(db, current_user.id, query)
    return habits


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific habit"""
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
    """Update a habit"""
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    
    habit = HabitService.update_habit(db, habit, habit_data)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a habit"""
    habit = HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    
    HabitService.delete_habit(db, habit)
    return None
