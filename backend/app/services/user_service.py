from sqlalchemy.orm import Session
from app.models import User
from app.auth.security import get_password_hash, verify_password
from app.schemas import UserCreate
import uuid
from typing import Optional

class UserService:
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        user = User(
            id=str(uuid.uuid4()),
            email=user_create.email,
            username=user_create.username,
            hashed_password=get_password_hash(user_create.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
