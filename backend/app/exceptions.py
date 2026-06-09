"""API Exception and error handling"""
from fastapi import HTTPException, status
from typing import Optional


class HabitTrackerException(Exception):
    """Base exception for Habit Tracker"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


class DuplicateHabitException(HabitTrackerException):
    """Raised when trying to create a habit with duplicate name"""
    def __init__(self):
        super().__init__(
            "A habit with this name already exists",
            status.HTTP_400_BAD_REQUEST
        )


class HabitNotFound(HabitTrackerException):
    """Raised when habit is not found"""
    def __init__(self):
        super().__init__("Habit not found", status.HTTP_404_NOT_FOUND)


class UserNotFound(HabitTrackerException):
    """Raised when user is not found"""
    def __init__(self):
        super().__init__("User not found", status.HTTP_404_NOT_FOUND)


class InvalidCredentials(HabitTrackerException):
    """Raised when login credentials are invalid"""
    def __init__(self):
        super().__init__(
            "Invalid email or password",
            status.HTTP_401_UNAUTHORIZED
        )


class UserAlreadyExists(HabitTrackerException):
    """Raised when user already exists"""
    def __init__(self, field: str = "User"):
        super().__init__(
            f"{field} already exists",
            status.HTTP_400_BAD_REQUEST
        )


class InvalidTokenException(HabitTrackerException):
    """Raised when token is invalid"""
    def __init__(self):
        super().__init__(
            "Invalid or expired token",
            status.HTTP_401_UNAUTHORIZED
        )


class CompletionAlreadyExists(HabitTrackerException):
    """Raised when completion already exists for date"""
    def __init__(self):
        super().__init__(
            "Habit already completed on this date",
            status.HTTP_400_BAD_REQUEST
        )


class PermissionDenied(HabitTrackerException):
    """Raised when user doesn't have permission"""
    def __init__(self):
        super().__init__(
            "You don't have permission to access this resource",
            status.HTTP_403_FORBIDDEN
        )
