from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class PcodSymptoms(BaseModel):
    cycle_irregularity: bool = False
    stubborn_weight: bool = False
    hirsutism: bool = False
    acne: bool = False
    acanthosis: bool = False


class UserProfileInput(BaseModel):
    age: int = Field(..., ge=1, le=120, description="Age in years")
    gender: str = Field(..., description="Male, Female, or Other")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    height_cm: float = Field(..., gt=0, description="Height in centimeters")
    fitness_goal: str = Field(
        ..., description="Weight Loss, Muscle Gain, Endurance, or Flexibility"
    )
    experience_level: str = Field(
        ..., description="Beginner, Intermediate, or Advanced"
    )
    equipment: str = Field(
        ..., description="None, Minimal, or Full Gym"
    )
    training_days_per_week: int = Field(..., ge=1, le=7)
    session_duration_min: int = Field(..., gt=0)
    pcod_symptoms: Optional[PcodSymptoms] = None

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        allowed = {"Male", "Female", "Other"}
        if v not in allowed:
            raise ValueError(f"gender must be one of {allowed}")
        return v

    @field_validator("fitness_goal")
    @classmethod
    def validate_fitness_goal(cls, v: str) -> str:
        allowed = {"Weight Loss", "Muscle Gain", "Endurance", "Flexibility"}
        if v not in allowed:
            raise ValueError(f"fitness_goal must be one of {allowed}")
        return v

    @field_validator("experience_level")
    @classmethod
    def validate_experience_level(cls, v: str) -> str:
        allowed = {"Beginner", "Intermediate", "Advanced"}
        if v not in allowed:
            raise ValueError(f"experience_level must be one of {allowed}")
        return v

    @field_validator("equipment")
    @classmethod
    def validate_equipment(cls, v: str) -> str:
        allowed = {"None", "Minimal", "Full Gym"}
        if v not in allowed:
            raise ValueError(f"equipment must be one of {allowed}")
        return v


class RiskFlag(BaseModel):
    title: str
    description: str
    severity: str  # "low", "medium", "high"


class ExerciseItem(BaseModel):
    name: str
    sets: int
    reps: str
    rest_seconds: int
    category: str
    muscle_group: Optional[str] = None


class HealthRiskResponse(BaseModel):
    cluster_id: int
    bmi: float
    bmi_category: str
    risk_flags: List[Dict[str, Any]]
    pcod_risk_score: Optional[float] = None
    pcod_risk_level: Optional[str] = None
    recommendations: List[str]
    workout_plan: List[Dict[str, Any]]
    plan_name: str
    quality_score: float
    # Template metadata for workout page display
    fitness_goal: Optional[str] = None
    experience_level: Optional[str] = None
    equipment: Optional[str] = None
    volume_score: Optional[float] = None
    intensity_score: Optional[float] = None


class WorkoutPlanResponse(BaseModel):
    plan_name: str
    quality_score: float
    exercises: List[ExerciseItem]


class UserCreateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    fitness_goal: str
    experience_level: str
    equipment: str
    training_days_per_week: int
    session_duration_min: int
    cluster_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    fitness_goal: str
    experience_level: str
    equipment: str
    training_days_per_week: int
    session_duration_min: int
    cluster_id: Optional[int]

    model_config = {"from_attributes": True}
