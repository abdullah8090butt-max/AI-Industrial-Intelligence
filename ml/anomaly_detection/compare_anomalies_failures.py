import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest


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


# Train on normal records
normal_train = train[train["Machine failure"] == 0]

model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
    n_jobs=-1
)

model.fit(normal_train[SENSOR_FEATURES])


# Detect anomalies
predictions = model.predict(test[SENSOR_FEATURES])

test["Anomaly"] = (predictions == -1).astype(int)


# Compare anomalies with failures
total_anomalies = test["Anomaly"].sum()
total_failures = test["Machine failure"].sum()

anomalous_failures = (
    (test["Anomaly"] == 1) &
    (test["Machine failure"] == 1)
).sum()

anomalous_normal = (
    (test["Anomaly"] == 1) &
    (test["Machine failure"] == 0)
).sum()


failure_detection_rate = (
    anomalous_failures / total_failures * 100
)

anomaly_failure_rate = (
    anomalous_failures / total_anomalies * 100
)


print("\n=== ANOMALY vs FAILURE ANALYSIS ===")

print(f"Total test records: {len(test)}")
print(f"Total anomalies: {total_anomalies}")
print(f"Total failures: {total_failures}")

print(f"\nAnomalies that were failures: {anomalous_failures}")
print(f"Anomalies that were normal: {anomalous_normal}")

print(
    f"\nFailure detection rate: "
    f"{failure_detection_rate:.2f}%"
)

print(
    f"Anomaly-to-failure rate: "
    f"{anomaly_failure_rate:.2f}%"
)

print("\n=== ANALYSIS COMPLETED ===")