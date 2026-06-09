from sqlalchemy.orm import Session
from app.models import Habit
from app.schemas import HabitCreate, HabitUpdate
import uuid
from typing import List, Optional

class HabitService:
    @staticmethod
    def create_habit(db: Session, user_id: str, habit_create: HabitCreate) -> Habit:
        """Create a new habit"""
        habit = Habit(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=habit_create.name,
            description=habit_create.description
        )
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit
    
    @staticmethod
    def get_habit_by_id(db: Session, habit_id: str) -> Optional[Habit]:
        """Get habit by ID"""
        return db.query(Habit).filter(Habit.id == habit_id).first()
    
    @staticmethod
    def get_user_habits(db: Session, user_id: str, active_only: bool = True) -> List[Habit]:
        """Get all habits for a user"""
        query = db.query(Habit).filter(Habit.user_id == user_id)
        if active_only:
            query = query.filter(Habit.is_active == True)
        return query.all()
    
    @staticmethod
    def update_habit(db: Session, habit_id: str, habit_update: HabitUpdate) -> Optional[Habit]:
        """Update a habit"""
        habit = HabitService.get_habit_by_id(db, habit_id)
        if not habit:
            return None
        
        update_data = habit_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(habit, key, value)
        
        db.commit()
        db.refresh(habit)
        return habit
    
    @staticmethod
    def delete_habit(db: Session, habit_id: str) -> bool:
        """Soft delete a habit"""
        habit = HabitService.get_habit_by_id(db, habit_id)
        if not habit:
            return False
        habit.is_active = False
        db.commit()
        return True
