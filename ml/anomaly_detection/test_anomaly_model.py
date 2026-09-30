import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Load training and test data
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


# Train only on normal records
normal_train = train[train["Machine failure"] == 0]

X_train = normal_train[SENSOR_FEATURES]
X_test = test[SENSOR_FEATURES]

y_test = test["Machine failure"]


# Build model
model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
    n_jobs=-1
)


# Train
model.fit(X_train)


# Predict
predictions = model.predict(X_test)

# Isolation Forest:
#  1  = normal
# -1  = anomaly
anomaly_predictions = (predictions == -1).astype(int)


print("\n=== ANOMALY PROOF-OF-CONCEPT ===")

print(f"Test samples: {len(X_test)}")
print(f"Detected anomalies: {anomaly_predictions.sum()}")
print(f"Actual failures: {y_test.sum()}")

print("\n=== CONFUSION MATRIX ===")
print(confusion_matrix(y_test, anomaly_predictions))

print("\n=== CLASSIFICATION REPORT ===")
print(
    classification_report(
        y_test,
        anomaly_predictions,
        target_names=["Normal", "Failure"],
        zero_division=0
    )
)

print("\n=== PROOF-OF-CONCEPT COMPLETED ===")