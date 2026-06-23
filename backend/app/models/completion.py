from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Completion(Base):
    __tablename__ = "completions"

    id = Column(String, primary_key=True, index=True)
    habit_id = Column(String, ForeignKey("habits.id"), nullable=False, index=True)
    completion_date = Column(Date, nullable=False, index=True)
    completed_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    habit = relationship("Habit", back_populates="completions")

    __table_args__ = (
        UniqueConstraint("habit_id", "completion_date", name="uq_habit_completion_date"),
    )
