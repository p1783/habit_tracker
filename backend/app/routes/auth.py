from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from app.services.user_service import UserService
from app.auth.security import verify_password, create_access_token
from app.exceptions import InvalidCredentials, UserAlreadyExists

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Returns:
        UserResponse: Created user data
    
    Raises:
        400: Email already registered or username already taken
    """
    try:
        user = UserService.create_user(db, user_data)
        return user
    except Exception as e:
        if "email" in str(e).lower():
            raise UserAlreadyExists("Email")
        elif "username" in str(e).lower():
            raise UserAlreadyExists("Username")
        raise


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and get access token
    
    Returns:
        Token: Access token for authentication
    
    Raises:
        401: Invalid credentials
        403: User account is inactive
    """
    user = UserService.get_user_by_email(db, user_data.email)
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise InvalidCredentials()
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }
