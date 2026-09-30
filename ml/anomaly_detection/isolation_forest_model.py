import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


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


# Use only normal training records
normal_train = train[train["Machine failure"] == 0]

X_normal = normal_train[SENSOR_FEATURES]


# Create Isolation Forest
model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
    n_jobs=-1
)


# Train model
model.fit(X_normal)


print("\n=== ISOLATION FOREST MODEL ===")
print(f"Normal training samples: {len(X_normal)}")
print(f"Sensor features: {len(SENSOR_FEATURES)}")
print(f"Trees: {model.n_estimators}")
print(f"Contamination: {model.contamination}")

print("\n=== MODEL TRAINING COMPLETED ===")