"""
FitAdapt ML — FastAPI Application
"""

import os
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
import models
from schemas import (
    UserProfileInput,
    HealthRiskResponse,
    UserCreateRequest,
    UserResponse,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"
TRAIN_SCRIPT = BASE_DIR / "ml" / "train_models.py"


def _ensure_artifacts():
    """Run training if artifacts are missing."""
    required = [
        ARTIFACTS_DIR / "kmeans_pipeline.joblib",
        ARTIFACTS_DIR / "rf_regressor.joblib",
        ARTIFACTS_DIR / "workout_templates.json",
    ]
    if not all(p.exists() for p in required):
        print("[startup] Artifacts missing — running training script...")
        result = subprocess.run(
            [sys.executable, str(TRAIN_SCRIPT)],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            raise RuntimeError("Training script failed. See logs above.")
        print("[startup] Training complete.")
    else:
        print("[startup] Artifacts found.")


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables (no-op if already exist; skips on connection failure)
    try:
        models.Base.metadata.create_all(bind=engine)
        print("[startup] DB tables ensured.")
    except Exception as exc:
        print(f"[startup] DB unavailable, skipping table creation: {exc}")

    # Ensure ML artifacts
    _ensure_artifacts()

    # Load predictor
    from ml.predictor import FitAdaptPredictor
    app.state.predictor = FitAdaptPredictor(str(ARTIFACTS_DIR))
    app.state.ml_loaded = True
    print("[startup] FitAdaptPredictor loaded.")

    yield

    # Cleanup
    app.state.ml_loaded = False
    print("[shutdown] FitAdapt ML API stopped.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="FitAdapt ML API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health_check():
    ml_loaded = getattr(app.state, "ml_loaded", False)
    return {"status": "ok", "ml_loaded": ml_loaded}


@app.post("/api/predict", response_model=HealthRiskResponse)
def predict(user_input: UserProfileInput):
    """Run ML pipeline and return health risk + workout plan."""
    predictor = app.state.predictor
    result = predictor.generate_full_response(user_input.model_dump())
    return result


@app.get("/api/workout-templates")
def get_workout_templates():
    """Return all available workout templates."""
    predictor = app.state.predictor
    return {"templates": predictor.workout_templates}


@app.post("/api/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    """Save a user profile to the database."""
    try:
        db_user = models.User(
            name=user_data.name,
            email=user_data.email,
            age=user_data.age,
            gender=user_data.gender,
            weight_kg=user_data.weight_kg,
            height_cm=user_data.height_cm,
            fitness_goal=user_data.fitness_goal,
            experience_level=user_data.experience_level,
            equipment=user_data.equipment,
            training_days_per_week=user_data.training_days_per_week,
            session_duration_min=user_data.session_duration_min,
            cluster_id=user_data.cluster_id,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")
