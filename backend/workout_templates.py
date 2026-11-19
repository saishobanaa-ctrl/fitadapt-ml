"""
workout_templates.py
--------------------
FitAdapt ML — Static Workout Template Library

Each template is a dictionary with:
  - id, name, goal, experience_level, equipment
  - volume_score (0-10): total weekly sets/reps load
  - intensity_score (0-10): average effort level
  - exercises: list of exercise dicts

Templates are matched to users via the Random Forest Regressor plan-quality scorer.
"""

WORKOUT_TEMPLATES = [
    # ─────────────────── WEIGHT LOSS ───────────────────
    {
        "id": "WL-BEG-HOME",
        "name": "Lean Start — Home Burn",
        "goal": "weight_loss",
        "experience_level": "beginner",
        "equipment": "home",
        "volume_score": 5,
        "intensity_score": 4,
        "exercises": [
            {"name": "Jumping Jacks",        "sets": 3, "reps": "30 reps",  "rest": "30s", "muscle": "Full Body"},
            {"name": "Bodyweight Squats",    "sets": 3, "reps": "15 reps",  "rest": "45s", "muscle": "Legs"},
            {"name": "Push-Ups",             "sets": 3, "reps": "10 reps",  "rest": "45s", "muscle": "Chest"},
            {"name": "High Knees",           "sets": 3, "reps": "40 reps",  "rest": "30s", "muscle": "Cardio"},
            {"name": "Plank Hold",           "sets": 3, "reps": "30s hold", "rest": "30s", "muscle": "Core"},
            {"name": "Glute Bridges",        "sets": 3, "reps": "15 reps",  "rest": "30s", "muscle": "Glutes"},
        ],
    },
    {
        "id": "WL-INT-HOME",
        "name": "Fat Torch — HIIT Circuit",
        "goal": "weight_loss",
        "experience_level": "intermediate",
        "equipment": "home",
        "volume_score": 7,
        "intensity_score": 8,
        "exercises": [
            {"name": "Burpees",              "sets": 4, "reps": "12 reps",  "rest": "30s", "muscle": "Full Body"},
            {"name": "Jump Squats",          "sets": 4, "reps": "15 reps",  "rest": "30s", "muscle": "Legs"},
            {"name": "Mountain Climbers",    "sets": 4, "reps": "30 reps",  "rest": "20s", "muscle": "Core"},
            {"name": "Push-Up to Shoulder Tap", "sets": 3, "reps": "12 reps", "rest": "45s", "muscle": "Chest/Core"},
            {"name": "Speed Skaters",        "sets": 3, "reps": "20 reps",  "rest": "30s", "muscle": "Legs/Cardio"},
            {"name": "Flutter Kicks",        "sets": 3, "reps": "40 reps",  "rest": "20s", "muscle": "Core"},
        ],
    },
    {
        "id": "WL-INT-GYM",
        "name": "Cardio-Strength Fusion",
        "goal": "weight_loss",
        "experience_level": "intermediate",
        "equipment": "gym",
        "volume_score": 7,
        "intensity_score": 7,
        "exercises": [
            {"name": "Treadmill Sprint Intervals", "sets": 5, "reps": "1 min on / 1 min off", "rest": "60s", "muscle": "Cardio"},
            {"name": "Goblet Squats",         "sets": 4, "reps": "12 reps", "rest": "45s", "muscle": "Legs"},
            {"name": "Cable Row",             "sets": 3, "reps": "12 reps", "rest": "45s", "muscle": "Back"},
            {"name": "Dumbbell Lunges",       "sets": 3, "reps": "10 each", "rest": "45s", "muscle": "Legs"},
            {"name": "Battle Ropes",          "sets": 3, "reps": "30s",     "rest": "30s", "muscle": "Full Body"},
            {"name": "Ab Crunch Machine",     "sets": 3, "reps": "15 reps", "rest": "30s", "muscle": "Core"},
        ],
    },
    {
        "id": "WL-ADV-GYM",
        "name": "Metabolic Conditioning Pro",
        "goal": "weight_loss",
        "experience_level": "advanced",
        "equipment": "gym",
        "volume_score": 9,
        "intensity_score": 9,
        "exercises": [
            {"name": "Barbell Deadlift",      "sets": 4, "reps": "8 reps",  "rest": "60s", "muscle": "Full Posterior"},
            {"name": "Box Jumps",             "sets": 4, "reps": "10 reps", "rest": "45s", "muscle": "Explosive Legs"},
            {"name": "Kettlebell Swings",     "sets": 4, "reps": "20 reps", "rest": "30s", "muscle": "Hips/Core"},
            {"name": "Pull-Ups",             "sets": 4, "reps": "10 reps",  "rest": "45s", "muscle": "Back/Biceps"},
            {"name": "Rowing Machine",        "sets": 3, "reps": "500m",    "rest": "90s", "muscle": "Full Body Cardio"},
            {"name": "Hanging Leg Raises",    "sets": 3, "reps": "15 reps", "rest": "30s", "muscle": "Core"},
        ],
    },

    # ─────────────────── MUSCLE GAIN ───────────────────
    {
        "id": "MG-BEG-HOME",
        "name": "Bodyweight Builder — Foundation",
        "goal": "muscle_gain",
        "experience_level": "beginner",
        "equipment": "home",
        "volume_score": 5,
        "intensity_score": 5,
        "exercises": [
            {"name": "Wide Push-Ups",         "sets": 4, "reps": "10 reps", "rest": "60s", "muscle": "Chest"},
            {"name": "Diamond Push-Ups",      "sets": 3, "reps": "8 reps",  "rest": "60s", "muscle": "Triceps"},
            {"name": "Bodyweight Squats",     "sets": 4, "reps": "20 reps", "rest": "60s", "muscle": "Quads"},
            {"name": "Reverse Lunges",        "sets": 3, "reps": "12 each", "rest": "45s", "muscle": "Hamstrings"},
            {"name": "Pike Push-Ups",         "sets": 3, "reps": "10 reps", "rest": "60s", "muscle": "Shoulders"},
            {"name": "Plank to Downdog",      "sets": 3, "reps": "10 reps", "rest": "30s", "muscle": "Core"},
        ],
    },
    {
        "id": "MG-INT-GYM",
        "name": "Hypertrophy Split — Push/Pull",
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "equipment": "gym",
        "volume_score": 8,
        "intensity_score": 7,
        "exercises": [
            {"name": "Bench Press",           "sets": 4, "reps": "10 reps", "rest": "75s", "muscle": "Chest"},
            {"name": "Incline Dumbbell Press","sets": 3, "reps": "10 reps", "rest": "60s", "muscle": "Upper Chest"},
            {"name": "Lat Pulldown",          "sets": 4, "reps": "10 reps", "rest": "75s", "muscle": "Back"},
            {"name": "Seated Cable Row",      "sets": 3, "reps": "12 reps", "rest": "60s", "muscle": "Mid Back"},
            {"name": "Overhead Press",        "sets": 3, "reps": "10 reps", "rest": "60s", "muscle": "Shoulders"},
            {"name": "Barbell Curl",          "sets": 3, "reps": "12 reps", "rest": "45s", "muscle": "Biceps"},
            {"name": "Tricep Rope Pushdown",  "sets": 3, "reps": "12 reps", "rest": "45s", "muscle": "Triceps"},
        ],
    },
    {
        "id": "MG-ADV-GYM",
        "name": "Power-Hypertrophy Elite",
        "goal": "muscle_gain",
        "experience_level": "advanced",
        "equipment": "gym",
        "volume_score": 10,
        "intensity_score": 9,
        "exercises": [
            {"name": "Barbell Back Squat",    "sets": 5, "reps": "5 reps",  "rest": "120s","muscle": "Legs/Full Body"},
            {"name": "Romanian Deadlift",     "sets": 4, "reps": "8 reps",  "rest": "90s", "muscle": "Hamstrings/Glutes"},
            {"name": "Weighted Pull-Ups",     "sets": 4, "reps": "8 reps",  "rest": "90s", "muscle": "Back/Biceps"},
            {"name": "Dumbbell Shoulder Press","sets": 4, "reps": "10 reps","rest": "60s", "muscle": "Shoulders"},
            {"name": "Incline Barbell Press", "sets": 4, "reps": "8 reps",  "rest": "90s", "muscle": "Chest"},
            {"name": "Leg Press",             "sets": 3, "reps": "12 reps", "rest": "75s", "muscle": "Quads"},
            {"name": "Cable Fly",             "sets": 3, "reps": "15 reps", "rest": "45s", "muscle": "Chest Isolation"},
        ],
    },

    # ─────────────────── ENDURANCE ───────────────────
    {
        "id": "EN-BEG-ANY",
        "name": "Endurance Foundation",
        "goal": "endurance",
        "experience_level": "beginner",
        "equipment": "home",
        "volume_score": 5,
        "intensity_score": 4,
        "exercises": [
            {"name": "Brisk Walk / Light Jog","sets": 1, "reps": "20 min",  "rest": "—",   "muscle": "Cardio"},
            {"name": "Step-Ups",              "sets": 3, "reps": "15 each", "rest": "30s", "muscle": "Legs"},
            {"name": "Arm Circles",           "sets": 2, "reps": "30s",     "rest": "15s", "muscle": "Shoulders"},
            {"name": "Wall Sit",              "sets": 3, "reps": "30s",     "rest": "30s", "muscle": "Quads"},
            {"name": "Low-Impact Jacks",      "sets": 3, "reps": "30 reps", "rest": "20s", "muscle": "Cardio"},
            {"name": "Deep Breathing Stretches", "sets": 2, "reps": "1 min","rest": "—",   "muscle": "Recovery"},
        ],
    },
    {
        "id": "EN-INT-GYM",
        "name": "Aerobic Power Builder",
        "goal": "endurance",
        "experience_level": "intermediate",
        "equipment": "gym",
        "volume_score": 7,
        "intensity_score": 7,
        "exercises": [
            {"name": "Stationary Bike Intervals","sets": 5,"reps": "3 min on / 1 min off","rest": "60s","muscle": "Cardio"},
            {"name": "Stair Climber",         "sets": 1, "reps": "15 min",  "rest": "—",   "muscle": "Legs/Cardio"},
            {"name": "Jump Rope",             "sets": 5, "reps": "1 min",   "rest": "30s", "muscle": "Full Body Cardio"},
            {"name": "Dumbbell Circuit (Squat + Press + Row)", "sets": 3, "reps": "15 reps each", "rest": "60s", "muscle": "Full Body"},
            {"name": "Core Stability Ball Exercises","sets": 3,"reps": "12 reps","rest": "30s","muscle": "Core"},
        ],
    },

    # ─────────────────── FLEXIBILITY ───────────────────
    {
        "id": "FL-BEG-HOME",
        "name": "Mobility & Flexibility Flow",
        "goal": "flexibility",
        "experience_level": "beginner",
        "equipment": "home",
        "volume_score": 3,
        "intensity_score": 2,
        "exercises": [
            {"name": "Cat-Cow Stretch",       "sets": 3, "reps": "10 reps", "rest": "15s", "muscle": "Spine"},
            {"name": "World's Greatest Stretch","sets": 2,"reps": "5 each", "rest": "15s", "muscle": "Full Body"},
            {"name": "Hip Flexor Lunge Stretch","sets": 2,"reps": "45s each","rest": "15s","muscle": "Hips"},
            {"name": "Seated Hamstring Stretch","sets": 2,"reps": "45s each","rest": "15s","muscle": "Hamstrings"},
            {"name": "Thoracic Rotation",     "sets": 2, "reps": "10 each", "rest": "15s", "muscle": "Upper Back"},
            {"name": "Child's Pose",          "sets": 3, "reps": "60s",     "rest": "—",   "muscle": "Back/Hips"},
            {"name": "Pigeon Pose",           "sets": 2, "reps": "60s each","rest": "15s", "muscle": "Glutes/Hip"},
        ],
    },

    # ─────────────────── GENERAL FITNESS ───────────────────
    {
        "id": "GF-BEG-HOME",
        "name": "All-Around Wellness — Beginner",
        "goal": "general_fitness",
        "experience_level": "beginner",
        "equipment": "home",
        "volume_score": 5,
        "intensity_score": 4,
        "exercises": [
            {"name": "March in Place",        "sets": 3, "reps": "1 min",   "rest": "20s", "muscle": "Warm-Up"},
            {"name": "Bodyweight Squats",     "sets": 3, "reps": "12 reps", "rest": "45s", "muscle": "Legs"},
            {"name": "Incline Push-Ups",      "sets": 3, "reps": "10 reps", "rest": "45s", "muscle": "Chest"},
            {"name": "Bent-Over Dumbbell Row","sets": 3, "reps": "12 reps", "rest": "45s", "muscle": "Back"},
            {"name": "Side Plank",            "sets": 2, "reps": "30s each","rest": "20s", "muscle": "Obliques"},
            {"name": "Bird-Dog",              "sets": 3, "reps": "10 each", "rest": "20s", "muscle": "Core/Stability"},
        ],
    },
    {
        "id": "GF-INT-GYM",
        "name": "Complete Fitness — Intermediate",
        "goal": "general_fitness",
        "experience_level": "intermediate",
        "equipment": "gym",
        "volume_score": 7,
        "intensity_score": 6,
        "exercises": [
            {"name": "Leg Press",             "sets": 3, "reps": "12 reps", "rest": "60s", "muscle": "Legs"},
            {"name": "Chest Press Machine",   "sets": 3, "reps": "12 reps", "rest": "60s", "muscle": "Chest"},
            {"name": "Assisted Pull-Up",      "sets": 3, "reps": "10 reps", "rest": "60s", "muscle": "Back"},
            {"name": "Shoulder Lateral Raise","sets": 3, "reps": "15 reps", "rest": "45s", "muscle": "Shoulders"},
            {"name": "Cable Crunch",          "sets": 3, "reps": "15 reps", "rest": "30s", "muscle": "Core"},
            {"name": "Treadmill Walk",        "sets": 1, "reps": "15 min",  "rest": "—",   "muscle": "Cardio"},
        ],
    },
]


def get_template_by_id(template_id: str) -> dict | None:
    """Return a single template dict by its ID."""
    for t in WORKOUT_TEMPLATES:
        if t["id"] == template_id:
            return t
    return None


def get_all_templates() -> list[dict]:
    """Return all workout templates."""
    return WORKOUT_TEMPLATES
