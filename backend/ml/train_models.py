"""
FitAdapt ML — Training Script
Generates synthetic data, trains KMeans + RandomForestRegressor,
saves artifacts to ml/artifacts/.
"""

import os
import json
import sys
import numpy as np
import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import silhouette_score, mean_squared_error, r2_score

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(SCRIPT_DIR, "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

KMEANS_PATH = os.path.join(ARTIFACTS_DIR, "kmeans_pipeline.joblib")
RF_PATH = os.path.join(ARTIFACTS_DIR, "rf_regressor.joblib")
TEMPLATES_PATH = os.path.join(ARTIFACTS_DIR, "workout_templates.json")

# ---------------------------------------------------------------------------
# 1. Generate synthetic user data
# ---------------------------------------------------------------------------
def generate_user_data(n: int = 500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    fitness_goals = ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility"]
    experience_levels = ["Beginner", "Intermediate", "Advanced"]
    equipments = ["None", "Minimal", "Full Gym"]

    df = pd.DataFrame({
        "age": rng.integers(18, 71, n).astype(float),
        "bmi": rng.uniform(16, 40, n),
        "training_days_per_week": rng.integers(1, 8, n).astype(float),
        "session_duration_min": rng.uniform(20, 90, n),
        "fitness_goal": rng.choice(fitness_goals, n),
        "experience_level": rng.choice(experience_levels, n),
        "equipment": rng.choice(equipments, n),
    })
    return df


# ---------------------------------------------------------------------------
# 2. Train KMeans clustering pipeline
# ---------------------------------------------------------------------------
def train_kmeans(df: pd.DataFrame):
    numerical_features = ["age", "bmi", "training_days_per_week", "session_duration_min"]
    categorical_features = ["fitness_goal", "experience_level", "equipment"]

    preprocessor = ColumnTransformer(transformers=[
        ("num", StandardScaler(), numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
    ])

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("kmeans", KMeans(n_clusters=5, random_state=42, n_init="auto")),
    ])

    pipeline.fit(df)
    labels = pipeline.named_steps["kmeans"].labels_
    transformed = pipeline.named_steps["preprocessor"].transform(df)
    score = silhouette_score(transformed, labels)
    print(f"[KMeans] Silhouette Score: {score:.4f}")

    joblib.dump(pipeline, KMEANS_PATH)
    print(f"[KMeans] Pipeline saved to {KMEANS_PATH}")
    return pipeline, labels


# ---------------------------------------------------------------------------
# 3. Train RandomForest plan-quality scorer
# ---------------------------------------------------------------------------
def train_rf(df: pd.DataFrame, cluster_labels: np.ndarray, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = len(df)

    volume_score = rng.uniform(0, 100, n)
    intensity_score = rng.uniform(0, 100, n)
    goal_match = rng.integers(0, 2, n).astype(float)
    experience_match = rng.integers(0, 2, n).astype(float)
    equipment_match = rng.integers(0, 2, n).astype(float)
    noise = rng.normal(0, 5, n)

    plan_quality_score = (
        volume_score * 0.3
        + intensity_score * 0.2
        + goal_match * 25
        + experience_match * 20
        + equipment_match * 15
        + cluster_labels * 2
        + noise
    )
    plan_quality_score = np.clip(plan_quality_score, 0, 100)

    X_rf = pd.DataFrame({
        "cluster_id": cluster_labels.astype(float),
        "volume_score": volume_score,
        "intensity_score": intensity_score,
        "goal_match": goal_match,
        "experience_match": experience_match,
        "equipment_match": equipment_match,
    })

    rf = RandomForestRegressor(n_estimators=100, random_state=seed)
    rf.fit(X_rf, plan_quality_score)

    preds = rf.predict(X_rf)
    rmse = np.sqrt(mean_squared_error(plan_quality_score, preds))
    r2 = r2_score(plan_quality_score, preds)
    print(f"[RF] RMSE: {rmse:.4f}  |  R² Score: {r2:.4f}")

    joblib.dump(rf, RF_PATH)
    print(f"[RF] Model saved to {RF_PATH}")
    return rf


# ---------------------------------------------------------------------------
# 4. Build and save workout template library
# ---------------------------------------------------------------------------
WORKOUT_TEMPLATES = [
    # -------------------------------------------------------------------------
    # Weight Loss templates
    # -------------------------------------------------------------------------
    {
        "template_id": 1,
        "name": "Cardio Kickstart",
        "fitness_goal": "Weight Loss",
        "experience_level": "Beginner",
        "equipment": "None",
        "volume_score": 60,
        "intensity_score": 50,
        "exercises": [
            {"name": "Jumping Jacks", "sets": 3, "reps": "30", "rest_seconds": 45, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "High Knees", "sets": 3, "reps": "40", "rest_seconds": 45, "category": "Cardio", "muscle_group": "Core/Legs"},
            {"name": "Bodyweight Squat", "sets": 3, "reps": "15", "rest_seconds": 60, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Push-Up (Knee)", "sets": 3, "reps": "10", "rest_seconds": 60, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Mountain Climbers", "sets": 3, "reps": "20", "rest_seconds": 45, "category": "Cardio", "muscle_group": "Core"},
            {"name": "Glute Bridge", "sets": 3, "reps": "15", "rest_seconds": 45, "category": "Strength", "muscle_group": "Glutes"},
        ],
    },
    {
        "template_id": 2,
        "name": "Fat Burn Circuit",
        "fitness_goal": "Weight Loss",
        "experience_level": "Intermediate",
        "equipment": "Minimal",
        "volume_score": 72,
        "intensity_score": 68,
        "exercises": [
            {"name": "Resistance Band Squat", "sets": 4, "reps": "15", "rest_seconds": 45, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Dumbbell Romanian Deadlift", "sets": 4, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Hamstrings"},
            {"name": "Burpees", "sets": 4, "reps": "10", "rest_seconds": 60, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Dumbbell Bent-Over Row", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Back"},
            {"name": "Jump Rope", "sets": 3, "reps": "60 sec", "rest_seconds": 45, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Plank", "sets": 3, "reps": "45 sec", "rest_seconds": 30, "category": "Core", "muscle_group": "Core"},
        ],
    },
    {
        "template_id": 3,
        "name": "HIIT Power Shred",
        "fitness_goal": "Weight Loss",
        "experience_level": "Advanced",
        "equipment": "Full Gym",
        "volume_score": 85,
        "intensity_score": 90,
        "exercises": [
            {"name": "Barbell Back Squat", "sets": 5, "reps": "8", "rest_seconds": 90, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Treadmill Sprint Intervals", "sets": 6, "reps": "30 sec on / 30 sec off", "rest_seconds": 30, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Cable Fly", "sets": 4, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Lat Pulldown", "sets": 4, "reps": "10", "rest_seconds": 60, "category": "Strength", "muscle_group": "Back"},
            {"name": "Leg Press", "sets": 4, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Battle Ropes", "sets": 4, "reps": "30 sec", "rest_seconds": 45, "category": "Cardio", "muscle_group": "Full Body"},
        ],
    },
    {
        "template_id": 4,
        "name": "Home Fat Blaster",
        "fitness_goal": "Weight Loss",
        "experience_level": "Intermediate",
        "equipment": "None",
        "volume_score": 68,
        "intensity_score": 72,
        "exercises": [
            {"name": "Squat Jump", "sets": 4, "reps": "12", "rest_seconds": 45, "category": "Plyometric", "muscle_group": "Quadriceps"},
            {"name": "Push-Up", "sets": 4, "reps": "15", "rest_seconds": 45, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Reverse Lunge", "sets": 3, "reps": "12 each", "rest_seconds": 45, "category": "Strength", "muscle_group": "Glutes"},
            {"name": "Tricep Dips (Chair)", "sets": 3, "reps": "12", "rest_seconds": 45, "category": "Strength", "muscle_group": "Triceps"},
            {"name": "Bicycle Crunches", "sets": 3, "reps": "20", "rest_seconds": 30, "category": "Core", "muscle_group": "Core"},
        ],
    },
    # -------------------------------------------------------------------------
    # Muscle Gain templates
    # -------------------------------------------------------------------------
    {
        "template_id": 5,
        "name": "Foundation Builder",
        "fitness_goal": "Muscle Gain",
        "experience_level": "Beginner",
        "equipment": "None",
        "volume_score": 55,
        "intensity_score": 45,
        "exercises": [
            {"name": "Push-Up", "sets": 3, "reps": "10", "rest_seconds": 60, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Bodyweight Squat", "sets": 3, "reps": "15", "rest_seconds": 60, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Pike Push-Up", "sets": 3, "reps": "8", "rest_seconds": 60, "category": "Strength", "muscle_group": "Shoulders"},
            {"name": "Reverse Lunge", "sets": 3, "reps": "10 each", "rest_seconds": 60, "category": "Strength", "muscle_group": "Glutes"},
            {"name": "Diamond Push-Up", "sets": 3, "reps": "8", "rest_seconds": 60, "category": "Strength", "muscle_group": "Triceps"},
            {"name": "Plank Hold", "sets": 3, "reps": "30 sec", "rest_seconds": 45, "category": "Core", "muscle_group": "Core"},
        ],
    },
    {
        "template_id": 6,
        "name": "Dumbbell Hypertrophy",
        "fitness_goal": "Muscle Gain",
        "experience_level": "Intermediate",
        "equipment": "Minimal",
        "volume_score": 78,
        "intensity_score": 72,
        "exercises": [
            {"name": "Dumbbell Bench Press", "sets": 4, "reps": "10", "rest_seconds": 90, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Dumbbell Romanian Deadlift", "sets": 4, "reps": "10", "rest_seconds": 90, "category": "Strength", "muscle_group": "Hamstrings"},
            {"name": "Dumbbell Shoulder Press", "sets": 4, "reps": "10", "rest_seconds": 90, "category": "Strength", "muscle_group": "Shoulders"},
            {"name": "Dumbbell Bent-Over Row", "sets": 4, "reps": "10", "rest_seconds": 90, "category": "Strength", "muscle_group": "Back"},
            {"name": "Dumbbell Curl", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Biceps"},
            {"name": "Dumbbell Tricep Kickback", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Triceps"},
        ],
    },
    {
        "template_id": 7,
        "name": "Powerlifting Mass",
        "fitness_goal": "Muscle Gain",
        "experience_level": "Advanced",
        "equipment": "Full Gym",
        "volume_score": 92,
        "intensity_score": 88,
        "exercises": [
            {"name": "Barbell Bench Press", "sets": 5, "reps": "5", "rest_seconds": 180, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Barbell Back Squat", "sets": 5, "reps": "5", "rest_seconds": 180, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Deadlift", "sets": 4, "reps": "4", "rest_seconds": 180, "category": "Strength", "muscle_group": "Full Body"},
            {"name": "Weighted Pull-Up", "sets": 4, "reps": "6", "rest_seconds": 120, "category": "Strength", "muscle_group": "Back"},
            {"name": "Barbell Overhead Press", "sets": 4, "reps": "6", "rest_seconds": 120, "category": "Strength", "muscle_group": "Shoulders"},
            {"name": "Barbell Curl", "sets": 3, "reps": "10", "rest_seconds": 90, "category": "Strength", "muscle_group": "Biceps"},
        ],
    },
    {
        "template_id": 8,
        "name": "Resistance Muscle Builder",
        "fitness_goal": "Muscle Gain",
        "experience_level": "Beginner",
        "equipment": "Minimal",
        "volume_score": 62,
        "intensity_score": 55,
        "exercises": [
            {"name": "Resistance Band Chest Press", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Resistance Band Row", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Back"},
            {"name": "Resistance Band Squat", "sets": 3, "reps": "15", "rest_seconds": 60, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Resistance Band Lateral Raise", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Shoulders"},
            {"name": "Resistance Band Curl", "sets": 3, "reps": "15", "rest_seconds": 45, "category": "Strength", "muscle_group": "Biceps"},
        ],
    },
    # -------------------------------------------------------------------------
    # Endurance templates
    # -------------------------------------------------------------------------
    {
        "template_id": 9,
        "name": "Endurance Base Build",
        "fitness_goal": "Endurance",
        "experience_level": "Beginner",
        "equipment": "None",
        "volume_score": 58,
        "intensity_score": 40,
        "exercises": [
            {"name": "Brisk Walking", "sets": 1, "reps": "20 min", "rest_seconds": 0, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Step Touch Side-to-Side", "sets": 3, "reps": "2 min", "rest_seconds": 60, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Wall Sit", "sets": 3, "reps": "30 sec", "rest_seconds": 45, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Calf Raises", "sets": 3, "reps": "20", "rest_seconds": 30, "category": "Strength", "muscle_group": "Calves"},
            {"name": "Bird Dog", "sets": 3, "reps": "10 each", "rest_seconds": 30, "category": "Core", "muscle_group": "Core"},
        ],
    },
    {
        "template_id": 10,
        "name": "Tempo Run & Strength",
        "fitness_goal": "Endurance",
        "experience_level": "Intermediate",
        "equipment": "Minimal",
        "volume_score": 75,
        "intensity_score": 65,
        "exercises": [
            {"name": "Jump Rope", "sets": 4, "reps": "2 min", "rest_seconds": 60, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Box Step-Up", "sets": 4, "reps": "12 each", "rest_seconds": 60, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Dumbbell Farmers Walk", "sets": 4, "reps": "30 m", "rest_seconds": 60, "category": "Strength", "muscle_group": "Full Body"},
            {"name": "Lateral Shuffle", "sets": 4, "reps": "30 sec", "rest_seconds": 45, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Dead Bug", "sets": 3, "reps": "10 each", "rest_seconds": 30, "category": "Core", "muscle_group": "Core"},
            {"name": "Reverse Lunge", "sets": 3, "reps": "12 each", "rest_seconds": 60, "category": "Strength", "muscle_group": "Glutes"},
        ],
    },
    {
        "template_id": 11,
        "name": "Elite Endurance Protocol",
        "fitness_goal": "Endurance",
        "experience_level": "Advanced",
        "equipment": "Full Gym",
        "volume_score": 88,
        "intensity_score": 82,
        "exercises": [
            {"name": "Rowing Machine", "sets": 1, "reps": "15 min", "rest_seconds": 0, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Cycling Intervals (Bike)", "sets": 6, "reps": "1 min hard / 1 min easy", "rest_seconds": 0, "category": "Cardio", "muscle_group": "Legs"},
            {"name": "Kettlebell Swing", "sets": 5, "reps": "20", "rest_seconds": 45, "category": "Strength", "muscle_group": "Full Body"},
            {"name": "Sled Push", "sets": 4, "reps": "20 m", "rest_seconds": 90, "category": "Strength", "muscle_group": "Full Body"},
            {"name": "Treadmill Hill Walk", "sets": 1, "reps": "10 min", "rest_seconds": 0, "category": "Cardio", "muscle_group": "Full Body"},
            {"name": "Hanging Knee Raise", "sets": 4, "reps": "15", "rest_seconds": 45, "category": "Core", "muscle_group": "Core"},
        ],
    },
    # -------------------------------------------------------------------------
    # Flexibility templates
    # -------------------------------------------------------------------------
    {
        "template_id": 12,
        "name": "Beginner Stretch & Flow",
        "fitness_goal": "Flexibility",
        "experience_level": "Beginner",
        "equipment": "None",
        "volume_score": 45,
        "intensity_score": 25,
        "exercises": [
            {"name": "Cat-Cow Stretch", "sets": 3, "reps": "10", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Spine"},
            {"name": "Child's Pose", "sets": 3, "reps": "45 sec", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Back"},
            {"name": "Standing Hamstring Stretch", "sets": 3, "reps": "30 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hamstrings"},
            {"name": "Hip Flexor Lunge Stretch", "sets": 3, "reps": "30 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hip Flexors"},
            {"name": "Seated Spinal Twist", "sets": 3, "reps": "30 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Spine"},
            {"name": "Downward Facing Dog", "sets": 3, "reps": "45 sec", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Full Body"},
        ],
    },
    {
        "template_id": 13,
        "name": "Yoga Power Flow",
        "fitness_goal": "Flexibility",
        "experience_level": "Intermediate",
        "equipment": "None",
        "volume_score": 55,
        "intensity_score": 40,
        "exercises": [
            {"name": "Sun Salutation A", "sets": 5, "reps": "1 round", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Full Body"},
            {"name": "Warrior I", "sets": 3, "reps": "45 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hips"},
            {"name": "Warrior II", "sets": 3, "reps": "45 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hips"},
            {"name": "Pigeon Pose", "sets": 2, "reps": "60 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Glutes"},
            {"name": "Bridge Pose", "sets": 3, "reps": "45 sec", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Spine"},
            {"name": "Half Moon Pose", "sets": 3, "reps": "30 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Full Body"},
        ],
    },
    {
        "template_id": 14,
        "name": "Advanced Mobility & Stretch",
        "fitness_goal": "Flexibility",
        "experience_level": "Advanced",
        "equipment": "Minimal",
        "volume_score": 65,
        "intensity_score": 50,
        "exercises": [
            {"name": "PNF Hamstring Stretch", "sets": 3, "reps": "30 sec hold + 10 sec contract", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hamstrings"},
            {"name": "Resistance Band Shoulder Dislocate", "sets": 3, "reps": "10", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Shoulders"},
            {"name": "Deep Squat Hold", "sets": 3, "reps": "60 sec", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hips"},
            {"name": "Standing Side Bend", "sets": 3, "reps": "45 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Obliques"},
            {"name": "Scorpion Stretch", "sets": 3, "reps": "30 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Spine"},
            {"name": "Full Body Foam Roll", "sets": 1, "reps": "5 min", "rest_seconds": 0, "category": "Recovery", "muscle_group": "Full Body"},
        ],
    },
    {
        "template_id": 15,
        "name": "Gym Stretch & Mobility",
        "fitness_goal": "Flexibility",
        "experience_level": "Advanced",
        "equipment": "Full Gym",
        "volume_score": 68,
        "intensity_score": 52,
        "exercises": [
            {"name": "Cable Hip Flexor Stretch", "sets": 3, "reps": "45 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Hip Flexors"},
            {"name": "Lat Stretch (Cable)", "sets": 3, "reps": "45 sec each", "rest_seconds": 15, "category": "Flexibility", "muscle_group": "Back"},
            {"name": "Incline Foam Roller Thoracic Ext.", "sets": 3, "reps": "60 sec", "rest_seconds": 15, "category": "Recovery", "muscle_group": "Spine"},
            {"name": "Seated Good Morning", "sets": 3, "reps": "15", "rest_seconds": 45, "category": "Strength", "muscle_group": "Hamstrings"},
            {"name": "Nordic Hamstring Curl", "sets": 3, "reps": "8", "rest_seconds": 90, "category": "Strength", "muscle_group": "Hamstrings"},
            {"name": "Reverse Hyper", "sets": 3, "reps": "15", "rest_seconds": 60, "category": "Strength", "muscle_group": "Glutes"},
        ],
    },
    {
        "template_id": 16,
        "name": "Beginner Gym Strength",
        "fitness_goal": "Muscle Gain",
        "experience_level": "Beginner",
        "equipment": "Full Gym",
        "volume_score": 65,
        "intensity_score": 55,
        "exercises": [
            {"name": "Machine Chest Press", "sets": 3, "reps": "12", "rest_seconds": 90, "category": "Strength", "muscle_group": "Chest"},
            {"name": "Lat Pulldown", "sets": 3, "reps": "12", "rest_seconds": 90, "category": "Strength", "muscle_group": "Back"},
            {"name": "Leg Press", "sets": 3, "reps": "15", "rest_seconds": 90, "category": "Strength", "muscle_group": "Quadriceps"},
            {"name": "Seated Dumbbell Curl", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Biceps"},
            {"name": "Tricep Rope Pushdown", "sets": 3, "reps": "12", "rest_seconds": 60, "category": "Strength", "muscle_group": "Triceps"},
            {"name": "Machine Shoulder Press", "sets": 3, "reps": "12", "rest_seconds": 90, "category": "Strength", "muscle_group": "Shoulders"},
        ],
    },
]


def save_templates():
    with open(TEMPLATES_PATH, "w", encoding="utf-8") as f:
        json.dump(WORKOUT_TEMPLATES, f, indent=2)
    print(f"[Templates] Saved {len(WORKOUT_TEMPLATES)} templates to {TEMPLATES_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("FitAdapt ML — Training Pipeline")
    print("=" * 60)

    print("\n[1/4] Generating synthetic user data (n=500)...")
    df = generate_user_data(n=500, seed=42)
    print(f"      Shape: {df.shape}")

    print("\n[2/4] Training KMeans clustering pipeline...")
    pipeline, cluster_labels = train_kmeans(df)

    print("\n[3/4] Training RandomForest plan-quality scorer...")
    rf = train_rf(df, cluster_labels, seed=42)

    print("\n[4/4] Saving workout templates library...")
    save_templates()

    print("\n" + "=" * 60)
    print("Training complete. Artifacts saved:")
    print(f"  {KMEANS_PATH}")
    print(f"  {RF_PATH}")
    print(f"  {TEMPLATES_PATH}")
    print("=" * 60)
