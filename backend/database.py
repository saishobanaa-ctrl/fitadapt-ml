"""
FitAdapt ML — Database Setup
Falls back to SQLite automatically if PostgreSQL is not available.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Use DATABASE_URL from environment, or fall back to SQLite (no setup needed)
DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    # SQLite fallback — works with zero configuration
    DB_PATH = Path(__file__).resolve().parent / "fitadapt.db"
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"[db] No DATABASE_URL set — using SQLite: {DB_PATH}")
else:
    # Normalize postgres:// → postgresql+psycopg2://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# SQLite needs check_same_thread=False for FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency: yields a DB session and closes on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
