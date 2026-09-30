import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "ml" / "anomaly_detection" / "saved_models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# Load training data
train = pd.read_csv(PROCESSED_DIR / "train.csv")


# Sensor features
SENSOR_FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# Train only on normal records
normal_train = train[train["Machine failure"] == 0]

X_normal = normal_train[SENSOR_FEATURES]


# Final model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)

model.fit(X_normal)


# Save model
model_path = MODEL_DIR / "isolation_forest.joblib"

joblib.dump(model, model_path)


print("\n=== FINAL ANOMALY MODEL SAVED ===")
print(f"Training samples: {len(X_normal)}")
print(f"Contamination: {model.contamination}")
print(f"Model path: {model_path}")

print("\n=== STEP 4.8 COMPLETED ===")