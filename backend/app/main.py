from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes import auth, habits, completions
from app.exceptions import HabitTrackerException
from app.handlers import habit_tracker_exception_handler, general_exception_handler


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Habit Tracker API",
    description="REST API for managing and tracking habits",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_exception_handler(HabitTrackerException, habit_tracker_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

allowed_origins = getattr(settings, "cors_origins", None) or [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(completions.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Habit Tracker API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
    }
