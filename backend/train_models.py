"""
train_models.py
---------------
FitAdapt ML -- Offline Machine Learning Training Script

This script is run ONCE (or whenever retraining is needed) to:
  1. Generate realistic synthetic training data
  2. Build the feature engineering pipeline (StandardScaler + OneHotEncoder)
  3. Train K-Means clustering and evaluate with Silhouette Score
  4. Train Random Forest Regressor and evaluate with RMSE + R2
  5. Serialize all artifacts to the /models directory via joblib

Run this before starting the FastAPI server:
  $ python train_models.py

Academic Evaluation Metrics:
  - K-Means: Silhouette Score (higher = better cluster separation)
  - Random Forest: RMSE (lower = less prediction error), R2 (higher = more variance explained)
"""

import os
import sys

# Force UTF-8 output on Windows to avoid encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import silhouette_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# -----------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

N_SAMPLES = 2000       # Synthetic training samples
N_CLUSTERS = 5         # K-Means cluster count
RANDOM_STATE = 42

SEP = "=" * 60

print(SEP)
print("  FitAdapt ML -- Training Pipeline Starting")
print(SEP)

# -----------------------------------------------------------------
# STEP 1: GENERATE SYNTHETIC TRAINING DATA
# -----------------------------------------------------------------

print("\n[1/4] Generating synthetic user data...")

np.random.seed(RANDOM_STATE)

ages = np.random.randint(16, 70, N_SAMPLES)
weights = np.random.uniform(45, 140, N_SAMPLES)         # kg
heights = np.random.uniform(150, 200, N_SAMPLES)        # cm
bmis = weights / (heights / 100) ** 2

# Correlated: higher BMI tends to correlate with fewer training days
training_days = np.clip(
    np.random.randint(0, 7, N_SAMPLES) - (bmis > 30).astype(int),
    0, 7
)
session_duration = np.random.choice([20, 30, 45, 60, 75, 90], N_SAMPLES)

goals = np.random.choice(
    ["weight_loss", "muscle_gain", "endurance", "flexibility", "general_fitness"],
    N_SAMPLES,
    p=[0.35, 0.30, 0.15, 0.10, 0.10],
)
experience_levels = np.random.choice(
    ["beginner", "intermediate", "advanced"],
    N_SAMPLES,
    p=[0.45, 0.40, 0.15],
)
equipment = np.random.choice(
    ["home", "gym"],
    N_SAMPLES,
    p=[0.45, 0.55],
)

user_df = pd.DataFrame({
    "age": ages,
    "bmi": bmis.round(2),
    "training_days": training_days,
    "session_duration": session_duration,
    "goal": goals,
    "experience_level": experience_levels,
    "equipment": equipment,
})

print(f"    [OK] Generated {N_SAMPLES} user profiles")
print(f"    [OK] BMI range: {bmis.min():.1f} - {bmis.max():.1f}")
print("    [OK] Goals distribution:")
print(user_df["goal"].value_counts().to_string())

# -----------------------------------------------------------------
# STEP 2: FEATURE ENGINEERING PIPELINE
# -----------------------------------------------------------------

print("\n[2/4] Building feature engineering pipeline...")

NUMERIC_FEATURES = ["age", "bmi", "training_days", "session_duration"]
CATEGORICAL_FEATURES = ["goal", "experience_level", "equipment"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
    ]
)

X_transformed = preprocessor.fit_transform(user_df)
print(f"    [OK] Transformed feature matrix shape: {X_transformed.shape}")
print(f"    [OK] Numeric features scaled: {NUMERIC_FEATURES}")
print(f"    [OK] Categorical features encoded: {CATEGORICAL_FEATURES}")

# Save preprocessor
joblib.dump(preprocessor, os.path.join(MODELS_DIR, "preprocessor.pkl"))
print("    [OK] Preprocessor saved --> models/preprocessor.pkl")

# -----------------------------------------------------------------
# STEP 3: UNSUPERVISED LEARNING -- K-MEANS CLUSTERING
# -----------------------------------------------------------------

print(f"\n[3/4] Training K-Means clustering (k={N_CLUSTERS})...")
print("    Evaluating Silhouette Scores for k = 2 to 7:")

best_k = N_CLUSTERS
best_silhouette = -1

for k in range(2, 8):
    km_temp = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    labels_temp = km_temp.fit_predict(X_transformed)
    s = silhouette_score(X_transformed, labels_temp)
    marker = " <- BEST" if s > best_silhouette else ""
    print(f"      k={k}: Silhouette Score = {s:.4f}{marker}")
    if s > best_silhouette:
        best_silhouette = s
        best_k = k

print(f"\n    [OK] Optimal k selected: {best_k}")

# Train final K-Means with best k
kmeans = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=10)
cluster_labels = kmeans.fit_predict(X_transformed)
final_silhouette = silhouette_score(X_transformed, cluster_labels)

print()
print("  +------------------------------------------+")
print("  |  K-MEANS EVALUATION                      |")
print(f"  |  Optimal k         : {best_k:<21}|")
print(f"  |  Silhouette Score  : {final_silhouette:<21.4f}|")
print("  |  (Range: -1 to 1; >0.5 = good clusters) |")
print("  +------------------------------------------+")

# Cluster size breakdown
unique, counts = np.unique(cluster_labels, return_counts=True)
print("    Cluster sizes:")
for cl, cnt in zip(unique, counts):
    bar = "#" * int(cnt / N_SAMPLES * 40)
    print(f"      Cluster {cl}: {cnt:4d} users ({cnt/N_SAMPLES*100:5.1f}%)  {bar}")

# Save K-Means model
joblib.dump(kmeans, os.path.join(MODELS_DIR, "kmeans_model.pkl"))
print("    [OK] K-Means model saved --> models/kmeans_model.pkl")

# Add cluster IDs back to dataframe for RF training
user_df["cluster_id"] = cluster_labels

# -----------------------------------------------------------------
# STEP 4: SUPERVISED LEARNING -- RANDOM FOREST REGRESSOR
# -----------------------------------------------------------------

print("\n[4/4] Training Random Forest Regressor (Plan Quality Scorer)...")

np.random.seed(RANDOM_STATE)

rf_rows = []
for idx, row in user_df.iterrows():
    for _ in range(3):
        volume_score = np.random.randint(2, 11)
        intensity_score = np.random.randint(2, 11)

        goal_match = np.random.choice([0, 1], p=[0.3, 0.7])
        experience_match = np.random.choice([0, 1], p=[0.3, 0.7])
        equipment_match = np.random.choice([0, 1], p=[0.25, 0.75])

        # Plan Quality Score (0-100):
        # Weighted sum of match flags + volume/intensity scores + cluster bonus
        base_score = (
            goal_match * 35
            + experience_match * 25
            + equipment_match * 20
            + (volume_score / 10) * 10
            + (intensity_score / 10) * 10
        )
        cluster_bonus = (row["cluster_id"] % 3) * 2
        noise = np.random.normal(0, 5)
        quality_score = float(np.clip(base_score + cluster_bonus + noise, 0, 100))

        rf_rows.append({
            "cluster_id": row["cluster_id"],
            "volume_score": volume_score,
            "intensity_score": intensity_score,
            "goal_match": goal_match,
            "experience_match": experience_match,
            "equipment_match": equipment_match,
            "quality_score": quality_score,
        })

rf_df = pd.DataFrame(rf_rows)
print(f"    [OK] Generated {len(rf_df)} template-match training samples")
print(f"    [OK] Quality Score stats: mean={rf_df['quality_score'].mean():.1f}, std={rf_df['quality_score'].std():.1f}")

RF_FEATURES = ["cluster_id", "volume_score", "intensity_score", "goal_match", "experience_match", "equipment_match"]
X_rf = rf_df[RF_FEATURES].values
y_rf = rf_df["quality_score"].values

X_train, X_test, y_train, y_test = train_test_split(
    X_rf, y_rf, test_size=0.2, random_state=RANDOM_STATE
)

# Train Random Forest
rf_model = RandomForestRegressor(
    n_estimators=150,
    max_depth=8,
    min_samples_leaf=5,
    random_state=RANDOM_STATE,
    n_jobs=-1,
)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred = rf_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print()
print("  +-------------------------------------------------+")
print("  |  RANDOM FOREST REGRESSOR EVALUATION             |")
print(f"  |  Training samples : {len(X_train):<28}|")
print(f"  |  Test samples     : {len(X_test):<28}|")
print(f"  |  RMSE             : {rmse:<28.4f}|")
print(f"  |  R2 Score         : {r2:<28.4f}|")
print("  |  (R2 closer to 1 = model explains more variance)|")
print("  +-------------------------------------------------+")

# Feature Importance
feature_importance = dict(zip(RF_FEATURES, rf_model.feature_importances_))
print("    Feature Importances:")
for feat, imp in sorted(feature_importance.items(), key=lambda x: -x[1]):
    bar = "#" * int(imp * 40)
    print(f"      {feat:<20}: {imp:.4f}  {bar}")

# Save RF model
joblib.dump(rf_model, os.path.join(MODELS_DIR, "rf_regressor.pkl"))
print("    [OK] RF Regressor saved --> models/rf_regressor.pkl")

# -----------------------------------------------------------------
# DONE
# -----------------------------------------------------------------

print()
print(SEP)
print("  [SUCCESS] ALL MODELS TRAINED AND SAVED SUCCESSFULLY!")
print(SEP)
print()
print("Artifacts saved to:", MODELS_DIR)
print("  - preprocessor.pkl   (StandardScaler + OneHotEncoder)")
print("  - kmeans_model.pkl   (K-Means Clustering)")
print("  - rf_regressor.pkl   (Random Forest Plan Quality Scorer)")
print()
print("Next step: start the FastAPI server with:")
print("  python -m uvicorn main:app --reload")
print(SEP)