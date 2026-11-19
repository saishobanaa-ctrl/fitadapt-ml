"""
FitAdapt ML — Predictor
Loads trained artifacts and provides inference methods.
"""

import os
import json
from typing import Optional, List, Tuple, Dict, Any

import numpy as np
import pandas as pd
import joblib


class FitAdaptPredictor:
    """Loads joblib artifacts + workout templates, provides inference API."""

    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir

        # Load KMeans pipeline
        kmeans_path = os.path.join(artifacts_dir, "kmeans_pipeline.joblib")
        self.kmeans_pipeline = joblib.load(kmeans_path)

        # Load RF regressor
        rf_path = os.path.join(artifacts_dir, "rf_regressor.joblib")
        self.rf_regressor = joblib.load(rf_path)

        # Load workout templates
        templates_path = os.path.join(artifacts_dir, "workout_templates.json")
        with open(templates_path, "r", encoding="utf-8") as f:
            self.workout_templates: List[Dict[str, Any]] = json.load(f)

    # ------------------------------------------------------------------
    # BMI helpers
    # ------------------------------------------------------------------
    def compute_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Calculate BMI from weight (kg) and height (cm)."""
        height_m = height_cm / 100.0
        return round(weight_kg / (height_m ** 2), 2)

    def get_bmi_category(self, bmi: float) -> str:
        """Return BMI category string."""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25.0:
            return "Normal Weight"
        elif bmi < 30.0:
            return "Overweight"
        else:
            return "Obese"

    # ------------------------------------------------------------------
    # Clustering
    # ------------------------------------------------------------------
    def predict_cluster(self, user_input: dict) -> int:
        """Predict KMeans cluster for a user.

        Expected keys in user_input:
            age, bmi, training_days_per_week, session_duration_min,
            fitness_goal, experience_level, equipment
        """
        df = pd.DataFrame([{
            "age": float(user_input["age"]),
            "bmi": float(user_input["bmi"]),
            "training_days_per_week": float(user_input["training_days_per_week"]),
            "session_duration_min": float(user_input["session_duration_min"]),
            "fitness_goal": user_input["fitness_goal"],
            "experience_level": user_input["experience_level"],
            "equipment": user_input["equipment"],
        }])
        cluster_id = int(self.kmeans_pipeline.predict(df)[0])
        return cluster_id

    # ------------------------------------------------------------------
    # Template scoring
    # ------------------------------------------------------------------
    def score_templates(
        self,
        cluster_id: int,
        fitness_goal: str,
        experience_level: str,
        equipment: str,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Score all workout templates using the RF regressor.

        Returns list of (template_dict, score) sorted descending by score.
        """
        scored = []
        for template in self.workout_templates:
            goal_match = 1.0 if template["fitness_goal"] == fitness_goal else 0.0
            exp_match = 1.0 if template["experience_level"] == experience_level else 0.0
            equip_match = 1.0 if template["equipment"] == equipment else 0.0

            X = pd.DataFrame([{
                "cluster_id": float(cluster_id),
                "volume_score": float(template["volume_score"]),
                "intensity_score": float(template["intensity_score"]),
                "goal_match": goal_match,
                "experience_match": exp_match,
                "equipment_match": equip_match,
            }])
            score = float(self.rf_regressor.predict(X)[0])
            scored.append((template, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    # ------------------------------------------------------------------
    # Health risk engine
    # ------------------------------------------------------------------
    def compute_health_risks(
        self,
        age: float,
        bmi: float,
        training_days: int,
        gender: str,
        pcod_symptoms: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """Compute health risk flags and recommendations."""
        risk_flags: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        # 1. Underweight
        if bmi < 18.5:
            risk_flags.append({
                "title": "Underweight",
                "description": (
                    "Your BMI indicates you are underweight. This can lead to "
                    "nutritional deficiencies, weakened immunity, and reduced "
                    "bone density."
                ),
                "severity": "low",
            })
            recommendations.append(
                "Consult a nutritionist to establish a calorie-surplus meal plan."
            )
            recommendations.append(
                "Focus on strength training to build lean muscle mass."
            )

        # 2. Overweight → insulin resistance risk
        if 25.0 <= bmi < 30.0:
            risk_flags.append({
                "title": "Overweight — Insulin Resistance Risk",
                "description": (
                    "A BMI in the overweight range is associated with increased "
                    "risk of insulin resistance, pre-diabetes, and metabolic "
                    "syndrome."
                ),
                "severity": "medium",
            })
            recommendations.append(
                "Aim for 150+ minutes of moderate-intensity cardio per week."
            )
            recommendations.append(
                "Reduce refined carbohydrate and added sugar intake."
            )

        # 3. Obese → Type-2 Diabetes + knee/joint load
        if bmi >= 30.0:
            risk_flags.append({
                "title": "Obesity — Type-2 Diabetes Risk",
                "description": (
                    "Obesity significantly elevates the risk of Type-2 Diabetes, "
                    "hypertension, and cardiovascular disease. Immediate lifestyle "
                    "intervention is recommended."
                ),
                "severity": "high",
            })
            risk_flags.append({
                "title": "Elevated Joint & Knee Load",
                "description": (
                    "Excess body weight places significant mechanical stress on "
                    "knee joints and the lumbar spine, increasing injury risk."
                ),
                "severity": "medium",
            })
            recommendations.append(
                "Begin with low-impact exercises (swimming, cycling, walking) "
                "to protect joints."
            )
            recommendations.append(
                "Work with a physician to create a medically supervised weight-loss plan."
            )

        # 4. Sedentary lifestyle
        if training_days < 3:
            risk_flags.append({
                "title": "Sedentary Lifestyle — Metabolic Syndrome Risk",
                "description": (
                    "Exercising fewer than 3 days per week is classified as "
                    "sedentary. This increases risk of metabolic syndrome, "
                    "depression, and cardiovascular disease."
                ),
                "severity": "medium",
            })
            recommendations.append(
                "Gradually increase activity to at least 3 sessions per week."
            )
            recommendations.append(
                "Break up prolonged sitting with 5-minute movement breaks every hour."
            )

        # 5. Age > 45 and BMI > 25 → cardiovascular risk
        if age > 45 and bmi > 25:
            risk_flags.append({
                "title": "Elevated Cardiovascular Risk",
                "description": (
                    "The combination of age over 45 and BMI above 25 significantly "
                    "elevates cardiovascular disease risk. Regular monitoring of "
                    "blood pressure and cholesterol is advised."
                ),
                "severity": "medium",
            })
            recommendations.append(
                "Schedule regular cardiovascular screenings (blood pressure, lipid panel)."
            )
            recommendations.append(
                "Include zone-2 cardio training 3–4 times per week."
            )

        # 6. PCOD/PCOS endocrine risk (female with any symptom)
        if gender == "Female" and pcod_symptoms:
            any_symptom = any(pcod_symptoms.get(k, False) for k in [
                "cycle_irregularity", "stubborn_weight", "hirsutism",
                "acne", "acanthosis"
            ])
            if any_symptom:
                pcod_score, pcod_level = self.compute_pcod_risk(pcod_symptoms)
                severity = "low" if pcod_level == "Low" else ("medium" if pcod_level == "Moderate" else "high")
                risk_flags.append({
                    "title": "PCOD/PCOS Endocrine Risk",
                    "description": (
                        f"You report symptoms associated with Polycystic Ovarian "
                        f"Disease/Syndrome. PCOD/PCOS Risk Score: {pcod_score:.0f}/100 "
                        f"({pcod_level} risk). Hormonal imbalance may affect "
                        f"metabolism, fertility, and cardiovascular health."
                    ),
                    "severity": severity,
                })
                recommendations.append(
                    "Consult a gynaecologist or endocrinologist for PCOS evaluation."
                )
                recommendations.append(
                    "Strength training and low-GI diet have shown benefit in PCOS management."
                )

        # General positive recommendation if no flags
        if not risk_flags:
            recommendations.append(
                "Great health profile! Maintain your current active lifestyle."
            )
            recommendations.append(
                "Continue balanced nutrition and regular strength + cardio training."
            )

        return {"risk_flags": risk_flags, "recommendations": recommendations}

    # ------------------------------------------------------------------
    # PCOD risk scorer
    # ------------------------------------------------------------------
    def compute_pcod_risk(self, pcod_symptoms: dict) -> Tuple[float, str]:
        """Compute PCOD/PCOS risk score and level.

        Score weights:
            cycle_irregularity: 25
            stubborn_weight:    20
            hirsutism:          20
            acne:               15
            acanthosis:         20
        """
        weights = {
            "cycle_irregularity": 25,
            "stubborn_weight": 20,
            "hirsutism": 20,
            "acne": 15,
            "acanthosis": 20,
        }
        score = sum(
            weights[key]
            for key in weights
            if pcod_symptoms.get(key, False)
        )
        if score < 30:
            level = "Low"
        elif score <= 60:
            level = "Moderate"
        else:
            level = "High"
        return float(score), level

    # ------------------------------------------------------------------
    # Full response generator
    # ------------------------------------------------------------------
    def generate_full_response(self, user_input: dict) -> dict:
        """Generate a complete HealthRiskResponse-compatible dict.

        Expected keys in user_input (all from UserProfileInput):
            age, gender, weight_kg, height_cm, fitness_goal,
            experience_level, equipment, training_days_per_week,
            session_duration_min, pcod_symptoms (optional dict)
        """
        # Compute BMI
        bmi = self.compute_bmi(user_input["weight_kg"], user_input["height_cm"])
        bmi_category = self.get_bmi_category(bmi)

        # Predict cluster
        cluster_input = {
            "age": user_input["age"],
            "bmi": bmi,
            "training_days_per_week": user_input["training_days_per_week"],
            "session_duration_min": user_input["session_duration_min"],
            "fitness_goal": user_input["fitness_goal"],
            "experience_level": user_input["experience_level"],
            "equipment": user_input["equipment"],
        }
        cluster_id = self.predict_cluster(cluster_input)

        # Score templates, pick best
        scored = self.score_templates(
            cluster_id=cluster_id,
            fitness_goal=user_input["fitness_goal"],
            experience_level=user_input["experience_level"],
            equipment=user_input["equipment"],
        )
        best_template, quality_score = scored[0]

        # Health risks
        pcod_symptoms = None
        if user_input.get("pcod_symptoms"):
            pcod_symptoms = user_input["pcod_symptoms"]
            if hasattr(pcod_symptoms, "model_dump"):
                pcod_symptoms = pcod_symptoms.model_dump()

        health = self.compute_health_risks(
            age=user_input["age"],
            bmi=bmi,
            training_days=user_input["training_days_per_week"],
            gender=user_input["gender"],
            pcod_symptoms=pcod_symptoms,
        )

        # PCOD risk score
        pcod_risk_score = None
        pcod_risk_level = None
        if user_input.get("gender") == "Female" and pcod_symptoms:
            any_symptom = any(pcod_symptoms.get(k, False) for k in [
                "cycle_irregularity", "stubborn_weight", "hirsutism",
                "acne", "acanthosis"
            ])
            if any_symptom:
                pcod_risk_score, pcod_risk_level = self.compute_pcod_risk(pcod_symptoms)

        return {
            "cluster_id": cluster_id,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "risk_flags": health["risk_flags"],
            "pcod_risk_score": pcod_risk_score,
            "pcod_risk_level": pcod_risk_level,
            "recommendations": health["recommendations"],
            "workout_plan": best_template["exercises"],
            "plan_name": best_template["name"],
            "quality_score": round(quality_score, 2),
            # Template metadata so the workout page can display goal/level/volume/intensity
            "fitness_goal": best_template.get("fitness_goal"),
            "experience_level": best_template.get("experience_level"),
            "equipment": best_template.get("equipment"),
            "volume_score": best_template.get("volume_score"),
            "intensity_score": best_template.get("intensity_score"),
        }
