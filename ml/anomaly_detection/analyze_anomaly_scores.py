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

X_train = normal_train[SENSOR_FEATURES]
X_test = test[SENSOR_FEATURES]


# Build and train model
model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train)


# Isolation Forest decision scores
scores = model.decision_function(X_test)

# Convert so that higher = more anomalous
anomaly_scores = -scores


print("\n=== ANOMALY SCORE ANALYSIS ===")

print("\nScore statistics:")
print(
    pd.Series(anomaly_scores).describe()
)

print("\nMost anomalous records:")

top_indices = anomaly_scores.argsort()[-10:][::-1]

for index in top_indices:
    print(
        f"Test index: {index} | "
        f"Anomaly score: {anomaly_scores[index]:.4f} | "
        f"Machine failure: {test.iloc[index]['Machine failure']}"
    )

print("\n=== ANOMALY SCORE ANALYSIS COMPLETED ===")