from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import HabitTrackerException


async def habit_tracker_exception_handler(request: Request, exc: HabitTrackerException):
    """Handle custom Habit Tracker exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status": "error"
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "status": "error"
        }
    )
