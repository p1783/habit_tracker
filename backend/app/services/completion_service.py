import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Completion
from app.schemas import CompletionCreate


class CompletionService:
    @staticmethod
    def create_completion(
        db: Session,
        habit_id: str,
        completion_create: CompletionCreate,
    ) -> Completion:
        completion = Completion(
            id=str(uuid.uuid4()),
            habit_id=habit_id,
            completion_date=completion_create.completion_date,
            notes=completion_create.notes,
        )
        db.add(completion)
        db.commit()
        db.refresh(completion)
        return completion

    @staticmethod
    def get_completion_by_id(
        db: Session,
        completion_id: str,
    ) -> Optional[Completion]:
        return db.query(Completion).filter(Completion.id == completion_id).first()

    @staticmethod
    def get_completion_by_date(
        db: Session,
        habit_id: str,
        completion_date: date,
    ) -> Optional[Completion]:
        return (
            db.query(Completion)
            .filter(
                Completion.habit_id == habit_id,
                Completion.completion_date == completion_date,
            )
            .first()
        )

    @staticmethod
    def get_completions_by_habit(
        db: Session,
        habit_id: str,
    ) -> List[Completion]:
        return (
            db.query(Completion)
            .filter(Completion.habit_id == habit_id)
            .order_by(Completion.completion_date.desc())
            .all()
        )

    @staticmethod
    def get_completions_by_date_range(
        db: Session,
        habit_id: str,
        start_date: date,
        end_date: date,
    ) -> List[Completion]:
        return (
            db.query(Completion)
            .filter(
                Completion.habit_id == habit_id,
                Completion.completion_date >= start_date,
                Completion.completion_date <= end_date,
            )
            .order_by(Completion.completion_date.desc())
            .all()
        )

    @staticmethod
    def delete_completion(db: Session, completion: Completion) -> None:
        db.delete(completion)
        db.commit()