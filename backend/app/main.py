from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="REST API for Habit Tracker application",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initialize database tables on application startup.

    For a student project this is acceptable.
    In production, migrations such as Alembic would be better.
    """
    init_db()


@app.get("/")
def root() -> dict:
    return {
        "message": "Habit Tracker API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
  
