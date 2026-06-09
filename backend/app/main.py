from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routes import auth, habits, completions
from app.exceptions import HabitTrackerException
from app.handlers import habit_tracker_exception_handler, general_exception_handler

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Habit Tracker API",
    description="REST API for managing and tracking habits",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add exception handlers
app.add_exception_handler(HabitTrackerException, habit_tracker_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(completions.router)


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Habit Tracker API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",
        "version": "0.1.0"
    }
