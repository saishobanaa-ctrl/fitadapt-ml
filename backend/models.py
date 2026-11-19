from datetime import datetime
from sqlalchemy import (
    Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    fitness_goal = Column(String(100), nullable=False)
    experience_level = Column(String(100), nullable=False)
    equipment = Column(String(100), nullable=False)
    training_days_per_week = Column(Integer, nullable=False)
    session_duration_min = Column(Integer, nullable=False)
    cluster_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workout_logs = relationship("WorkoutLog", back_populates="user")


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_name = Column(String(255), nullable=False)
    quality_score = Column(Float, nullable=False)
    completed_exercises = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workout_logs")
