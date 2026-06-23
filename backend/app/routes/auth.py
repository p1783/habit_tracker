from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, verify_password
from app.database import get_db
from app.exceptions import InvalidCredentials, UserAlreadyExists
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.create_user(db, user_data)
    except Exception as e:
        message = str(e).lower()

        if "email" in message:
            raise UserAlreadyExists("Email")
        if "username" in message:
            raise UserAlreadyExists("Username")

        raise


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise InvalidCredentials()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }