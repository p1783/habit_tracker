import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Habit
from app.schemas import HabitCreate, HabitUpdate


class HabitService:
    @staticmethod
    def create_habit(db: Session, user_id: str, habit_create: HabitCreate) -> Habit:
        habit = Habit(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=habit_create.name,
            description=habit_create.description,
            is_active=True,
        )
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def get_habit_by_id(
        db: Session,
        habit_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Habit]:
        query = db.query(Habit).filter(Habit.id == habit_id)

        if user_id is not None:
            query = query.filter(Habit.user_id == user_id)

        return query.first()

    @staticmethod
    def get_user_habits(
        db: Session,
        user_id: str,
        is_active: Optional[bool] = None,
    ) -> List[Habit]:
        query = db.query(Habit).filter(Habit.user_id == user_id)

        if is_active is not None:
            query = query.filter(Habit.is_active == is_active)

        return query.order_by(Habit.created_at.desc()).all()

    @staticmethod
    def search_habits(db: Session, user_id: str, query_text: str) -> List[Habit]:
        return (
            db.query(Habit)
            .filter(
                Habit.user_id == user_id,
                Habit.name.ilike(f"%{query_text}%"),
            )
            .order_by(Habit.created_at.desc())
            .all()
        )

    @staticmethod
    def update_habit(
        db: Session,
        habit: Habit,
        habit_update: HabitUpdate,
    ) -> Habit:
        update_data = habit_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(habit, key, value)

        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def delete_habit(db: Session, habit: Habit) -> None:
        db.delete(habit)
        db.commit()