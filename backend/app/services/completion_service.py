from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Completion
from app.schemas import CompletionCreate
from datetime import date, datetime, timedelta
import uuid
from typing import List, Optional

class CompletionService:
    @staticmethod
    def create_completion(db: Session, habit_id: str, completion_create: CompletionCreate) -> Completion:
        """Create a new completion record"""
        completion = Completion(
            id=str(uuid.uuid4()),
            habit_id=habit_id,
            completion_date=completion_create.completion_date,
            notes=completion_create.notes
        )
        db.add(completion)
        db.commit()
        db.refresh(completion)
        return completion
    
    @staticmethod
    def get_completion_by_id(db: Session, completion_id: str) -> Optional[Completion]:
        """Get completion by ID"""
        return db.query(Completion).filter(Completion.id == completion_id).first()
    
    @staticmethod
    def get_habit_completions(db: Session, habit_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Completion]:
        """Get completions for a habit within a date range"""
        query = db.query(Completion).filter(Completion.habit_id == habit_id)
        
        if start_date:
            query = query.filter(Completion.completion_date >= start_date)
        if end_date:
            query = query.filter(Completion.completion_date <= end_date)
        
        return query.order_by(Completion.completion_date.desc()).all()
    
    @staticmethod
    def get_habit_completions_this_week(db: Session, habit_id: str) -> List[Completion]:
        """Get completions for a habit in the current week"""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        return CompletionService.get_habit_completions(db, habit_id, start_of_week, end_of_week)
    
    @staticmethod
    def is_habit_completed_today(db: Session, habit_id: str) -> bool:
        """Check if habit is completed today"""
        today = date.today()
        completion = db.query(Completion).filter(
            and_(
                Completion.habit_id == habit_id,
                Completion.completion_date == today
            )
        ).first()
        return completion is not None
    
    @staticmethod
    def delete_completion(db: Session, completion_id: str) -> bool:
        """Delete a completion record"""
        completion = CompletionService.get_completion_by_id(db, completion_id)
        if not completion:
            return False
        db.delete(completion)
        db.commit()
        return True
