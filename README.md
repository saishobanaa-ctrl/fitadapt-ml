# FitAdapt ML 🤖💪
### AI-Powered Personalized Workout Generator & Preventative Health Risk Predictor

> A full-stack ML web application built for a 3rd-year Machine Learning curriculum.

---

## 🧠 ML Pipeline Overview

| Component | Algorithm | Metric |
|---|---|---|
| User Clustering | K-Means (k=5) | Silhouette Score: 0.117 |
| Plan Scoring | Random Forest Regressor (100 trees) | R²: 0.988, RMSE: 2.26 |
| Health Risk Engine | Rule-based heuristics | BMI + activity thresholds |
| PCOD/PCOS Screening | Weighted symptom scoring | 5-indicator endocrine score |

---

## 🛠 Tech Stack

- **Frontend:** React (Vite) + Tailwind CSS — dark-mode high-tech UI
- **Backend:** Python + FastAPI — RESTful API with lifespan model loading
- **ML:** Scikit-Learn (KMeans, RandomForestRegressor, StandardScaler, OneHotEncoder, joblib)
- **Database:** SQLite (dev) / PostgreSQL (prod) via SQLAlchemy ORM

---

## 🚀 Setup & Run

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
python ml/train_models.py          # Train ML models (run once)
python -m uvicorn main:app --reload
```
API runs at: http://127.0.0.1:8000  
Swagger docs: http://127.0.0.1:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs at: http://localhost:5173

---

## 📁 Project Structure

```
fitadapt-ml/
├── backend/
│   ├── main.py              # FastAPI app + lifespan model loading
│   ├── schemas.py           # Pydantic v2 request/response models
│   ├── models.py            # SQLAlchemy ORM (User, WorkoutLog)
│   ├── database.py          # SQLite/PostgreSQL engine setup
│   ├── requirements.txt
│   └── ml/
│       ├── train_models.py  # K-Means + Random Forest training (500 samples)
│       ├── predictor.py     # FitAdaptPredictor inference class
│       └── artifacts/       # joblib model files (auto-generated)
└── frontend/
    └── src/
        ├── pages/
        │   ├── Home.jsx            # Landing page with ML feature cards
        │   ├── HealthPredictor.jsx # Form + risk analysis + PCOD module
        │   └── MyWorkout.jsx       # Interactive exercise checklist
        ├── components/
        └── api/fitadaptApi.js
```

---

## 🎓 Academic Defense Points

1. **Hybrid ML Architecture** — Unsupervised (K-Means clustering) + Supervised (RF regression)
2. **Feature Engineering** — ColumnTransformer combining StandardScaler + OneHotEncoder
3. **Model Serialization** — joblib for offline training + online inference (zero retraining per request)
4. **Preventative Healthcare** — Bridges fitness AI with metabolic risk awareness and women's endocrine health (PCOD/PCOS)
5. **Production Pattern** — FastAPI lifespan context manager loads models once at startup
