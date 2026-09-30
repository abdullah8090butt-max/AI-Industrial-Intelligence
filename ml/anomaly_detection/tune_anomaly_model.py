import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Load data
train = pd.read_csv(PROCESSED_DIR / "train.csv")
test = pd.read_csv(PROCESSED_DIR / "test.csv")


# Sensor features
SENSOR_FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# Train on normal records only
normal_train = train[train["Machine failure"] == 0]

X_train = normal_train[SENSOR_FEATURES]
X_test = test[SENSOR_FEATURES]
y_test = test["Machine failure"]


# Test one targeted adjustment
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train)


# Predict anomalies
predictions = model.predict(X_test)
anomaly_predictions = (predictions == -1).astype(int)


# Metrics
precision = precision_score(
    y_test,
    anomaly_predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    anomaly_predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    anomaly_predictions,
    zero_division=0
)


print("\n=== ANOMALY MODEL TUNING ===")

print("Baseline contamination: 0.03")
print("Test contamination: 0.05")

print(f"\nDetected anomalies: {anomaly_predictions.sum()}")
print(f"Actual failures: {y_test.sum()}")

print(f"\nPrecision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-score: {f1:.3f}")

print("\n=== TUNING COMPLETED ===")