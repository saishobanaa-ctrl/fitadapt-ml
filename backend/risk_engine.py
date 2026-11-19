"""
risk_engine.py
--------------
FitAdapt ML — Preventative Health Risk Stratification Engine

Modules:
  1. compute_bmi()          — BMI calculation and obesity tier classification
  2. metabolic_risk()       — Insulin resistance / T2 Diabetes risk stratification
  3. joint_stress_risk()    — Patellar/knee and spinal load risk from BMI + activity mismatch
  4. pcod_pcos_risk()       — Women's endocrine screening (PCOD/PCOS indicators)
  5. compute_full_risk()    — Unified entry point returning the complete risk report
"""

from __future__ import annotations


# ─────────────────────────────────────────────────────────────
# 1. BMI CALCULATOR
# ─────────────────────────────────────────────────────────────

def compute_bmi(weight_kg: float, height_cm: float) -> dict:
    """
    Compute Body Mass Index and return classification tier.

    BMI = weight(kg) / height(m)^2
    WHO Classification:
      < 18.5   → Underweight
      18.5–24.9 → Normal
      25.0–29.9 → Overweight
      30.0–34.9 → Obese Class I
      35.0–39.9 → Obese Class II
      ≥ 40.0   → Obese Class III (Morbid)
    """
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "blue"
    elif bmi < 25.0:
        category = "Normal"
        color = "green"
    elif bmi < 30.0:
        category = "Overweight"
        color = "yellow"
    elif bmi < 35.0:
        category = "Obese Class I"
        color = "orange"
    elif bmi < 40.0:
        category = "Obese Class II"
        color = "red"
    else:
        category = "Obese Class III (Morbid)"
        color = "red"

    return {"bmi": bmi, "category": category, "color": color}


# ─────────────────────────────────────────────────────────────
# 2. METABOLIC / DIABETES RISK
# ─────────────────────────────────────────────────────────────

def metabolic_risk(bmi: float, age: int, training_days: int) -> dict:
    """
    Stratify prospective Type-2 Diabetes and Insulin Resistance risk.

    Risk factors considered:
      - BMI > 25 (overweight threshold)
      - Age > 35 (metabolic slowdown phase)
      - Training days < 3 (sedentary lifestyle marker)

    Score: 0–3 risk factors mapped to Low / Moderate / High
    """
    score = 0
    factors = []

    if bmi >= 30:
        score += 2
        factors.append("BMI indicates obesity — primary driver of insulin resistance")
    elif bmi >= 25:
        score += 1
        factors.append("BMI in overweight range — elevated visceral fat risk")

    if age >= 45:
        score += 2
        factors.append("Age ≥ 45: pancreatic beta-cell efficiency declines significantly")
    elif age >= 35:
        score += 1
        factors.append("Age ≥ 35: early metabolic slowdown phase begins")

    if training_days == 0:
        score += 2
        factors.append("Completely sedentary lifestyle — highest diabetes risk category")
    elif training_days < 3:
        score += 1
        factors.append("Low physical activity (<3 days/week) — reduced glucose uptake")

    if score == 0:
        level = "Low"
        message = "Your metabolic profile looks healthy. Keep up the active lifestyle!"
    elif score <= 2:
        level = "Moderate"
        message = "You show early markers for metabolic risk. Regular exercise and a low-glycemic diet are your best defense."
    else:
        level = "High"
        message = "Multiple risk factors detected for insulin resistance and Type-2 Diabetes. We strongly recommend starting an exercise routine TODAY and consulting a physician."

    return {
        "risk_level": level,
        "score": score,
        "factors": factors,
        "message": message,
        "condition": "Type-2 Diabetes / Insulin Resistance",
    }


# ─────────────────────────────────────────────────────────────
# 3. JOINT STRESS RISK
# ─────────────────────────────────────────────────────────────

def joint_stress_risk(bmi: float, age: int, training_days: int, session_duration: int) -> dict:
    """
    Evaluate patellar (knee), lumbar (lower back), and hip joint stress risk.

    Two scenarios:
      A. Obese + sedentary → degenerative joint load from excess weight with no muscular support
      B. High training frequency + long sessions → overuse injury and cartilage wear risk
    """
    score = 0
    factors = []

    # Excess weight load on joints
    if bmi >= 35:
        score += 3
        factors.append("Severe obesity: each kilogram adds ~4× force on knee joints — high degenerative risk")
    elif bmi >= 30:
        score += 2
        factors.append("Obesity significantly increases patellar compression and lumbar disc pressure")
    elif bmi >= 27:
        score += 1
        factors.append("Moderate overweight: elevated knee joint load, especially on stairs and inclines")

    # Overtraining risk
    weekly_volume = training_days * session_duration
    if weekly_volume > 500:  # >500 min/week
        score += 2
        factors.append("High training volume (>500 min/week): elevated risk for stress fractures and tendinopathy")
    elif weekly_volume > 350:
        score += 1
        factors.append("Above-average weekly training volume — monitor for overuse signs (soreness, swelling)")

    # Age-related cartilage degeneration
    if age >= 50:
        score += 2
        factors.append("Age ≥ 50: articular cartilage regeneration significantly reduced")
    elif age >= 40:
        score += 1
        factors.append("Age ≥ 40: begin joint-supportive exercises; avoid high-impact repetitive loading")

    if score == 0:
        level = "Low"
        message = "Your joint health indicators look good. Continue strength training to protect your joints long-term."
    elif score <= 3:
        level = "Moderate"
        message = "Some joint stress risk identified. Include mobility work, avoid high-impact activities on consecutive days."
    else:
        level = "High"
        message = "Significant joint stress risk! Prioritize low-impact training (swimming, cycling), weight management, and consult an orthopedic specialist."

    return {
        "risk_level": level,
        "score": score,
        "factors": factors,
        "message": message,
        "condition": "Joint Strain / Osteoarthritis Predisposition",
    }


# ─────────────────────────────────────────────────────────────
# 4. PCOD / PCOS SCREENING MODULE (Women Only)
# ─────────────────────────────────────────────────────────────

def pcod_pcos_risk(indicators: dict) -> dict:
    """
    Women's Endocrine Screening Module.

    Evaluates 6 clinical PCOD/PCOS indicators:
      - irregular_cycles: Menstrual cycle irregularity (>35 days or <21 days)
      - weight_retention:  Difficulty losing weight despite effort
      - hirsutism:         Excess facial/body hair growth
      - acne_severity:     Persistent hormonal acne (jaw, chin, back)
      - skin_darkening:    Acanthosis nigricans (dark patches at neck, underarms)
      - fatigue_levels:    Chronic unexplained fatigue / energy crashes

    Each indicator contributes 1 point to the endocrine risk score (max 6).
    """
    indicator_keys = [
        "irregular_cycles",
        "weight_retention",
        "hirsutism",
        "acne_severity",
        "skin_darkening",
        "fatigue_levels",
    ]

    indicator_labels = {
        "irregular_cycles":  "Irregular Menstrual Cycles",
        "weight_retention":  "Stubborn Weight Retention",
        "hirsutism":         "Excess Facial/Body Hair (Hirsutism)",
        "acne_severity":     "Persistent Hormonal Acne",
        "skin_darkening":    "Skin Darkening / Acanthosis Nigricans",
        "fatigue_levels":    "Chronic Fatigue & Energy Crashes",
    }

    positive_indicators = []
    score = 0

    for key in indicator_keys:
        if indicators.get(key, False):
            score += 1
            positive_indicators.append(indicator_labels[key])

    # Clinical risk stratification
    if score == 0:
        level = "Low"
        message = "No significant PCOD/PCOS indicators detected at this time. Maintain a balanced diet rich in anti-inflammatory foods and regular exercise."
        recommendation = "Annual gynecological checkup recommended."
    elif score <= 2:
        level = "Moderate"
        message = "You show 1–2 indicators associated with hormonal imbalance. This does not confirm PCOD/PCOS diagnosis but warrants attention."
        recommendation = "Consider consulting a gynecologist or endocrinologist for hormonal panel testing (LH/FSH ratio, AMH, Testosterone, Insulin)."
    elif score <= 4:
        level = "High"
        message = "Multiple PCOD/PCOS indicators detected. These symptoms strongly suggest a hormonal imbalance requiring professional evaluation."
        recommendation = "Schedule an ultrasound (transvaginal sonography) and full hormonal panel. Begin a low-glycemic diet and resistance training — both are clinically proven to improve PCOD/PCOS outcomes."
    else:
        level = "Very High"
        message = "5–6 indicators of PCOD/PCOS detected. This is a significant endocrine risk profile. Exercise is one of the most effective non-pharmacological interventions."
        recommendation = "Urgent: Consult a gynecologist/endocrinologist. Begin structured exercise immediately — studies show 150 min/week of moderate aerobic activity improves insulin sensitivity and regularizes cycles in PCOD/PCOS patients."

    return {
        "risk_level": level,
        "score": score,
        "max_score": 6,
        "positive_indicators": positive_indicators,
        "message": message,
        "recommendation": recommendation,
        "condition": "PCOD / PCOS Endocrine Screening",
    }


# ─────────────────────────────────────────────────────────────
# 5. UNIFIED RISK ENTRY POINT
# ─────────────────────────────────────────────────────────────

def compute_full_risk(
    age: int,
    gender: str,
    weight_kg: float,
    height_cm: float,
    training_days: int,
    session_duration: int,
    pcod_indicators: dict | None = None,
) -> dict:
    """
    Compute the complete health risk report for a user.

    Returns a dict containing:
      - bmi_info: BMI value and classification
      - metabolic: T2 Diabetes / insulin resistance risk
      - joint: Joint stress risk
      - pcod (optional): PCOD/PCOS endocrine screening result
      - overall_risk: Highest risk level across all modules
      - motivational_message: Personalized call to action
    """
    bmi_info = compute_bmi(weight_kg, height_cm)
    bmi = bmi_info["bmi"]

    metabolic = metabolic_risk(bmi, age, training_days)
    joint = joint_stress_risk(bmi, age, training_days, session_duration)

    risk_levels = {"Low": 0, "Moderate": 1, "High": 2, "Very High": 3}
    max_risk_score = max(
        risk_levels.get(metabolic["risk_level"], 0),
        risk_levels.get(joint["risk_level"], 0),
    )

    result = {
        "bmi_info": bmi_info,
        "metabolic": metabolic,
        "joint": joint,
        "pcod": None,
    }

    if gender.lower() in ["female", "f"] and pcod_indicators:
        pcod = pcod_pcos_risk(pcod_indicators)
        result["pcod"] = pcod
        max_risk_score = max(max_risk_score, risk_levels.get(pcod["risk_level"], 0))

    # Reverse map to get overall level
    reverse_map = {0: "Low", 1: "Moderate", 2: "High", 3: "Very High"}
    overall_level = reverse_map[max_risk_score]

    if overall_level == "Low":
        motivational = "Your health indicators are looking great! 💪 Starting your workout plan today will keep you at peak performance."
    elif overall_level == "Moderate":
        motivational = "You have manageable risk factors. The best time to act was yesterday — the second best time is NOW. Start your workout plan today!"
    elif overall_level == "High":
        motivational = "Your health risk analysis reveals significant risk factors. Exercise is your most powerful medicine. Start doing your exercises TODAY — every session counts!"
    else:
        motivational = "Your risk profile requires urgent lifestyle intervention. Exercise, alongside medical guidance, is clinically proven to reverse many of these risk factors. Begin NOW — your future self depends on it!"

    result["overall_risk"] = overall_level
    result["motivational_message"] = motivational

    return result
