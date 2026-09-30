import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "ml" / "predictive_maintenance" / "saved_models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(PROCESSED_DIR / "train.csv")

FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]",
    "categorical__Type_0",
    "categorical__Type_1",
    "categorical__Type_2"
]

TARGET = "Machine failure"
THRESHOLD = 0.40

X_train = train[FEATURES]
y_train = train[TARGET]

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

model_data = {
    "model": model,
    "threshold": THRESHOLD,
    "features": FEATURES,
    "target": TARGET
}

OUTPUT_FILE = MODEL_DIR / "random_forest_failure_model.joblib"

joblib.dump(model_data, OUTPUT_FILE)

print("\n=== FINAL FAILURE MODEL SAVED ===")
print(f"Model: {OUTPUT_FILE}")
print(f"Threshold: {THRESHOLD}")
print(f"Features: {len(FEATURES)}")
print("\n=== MODEL SAVE COMPLETED ===")