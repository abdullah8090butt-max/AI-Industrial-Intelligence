import joblib
import pandas as pd
from pathlib import Path

from recommendation_service import RecommendationService


BASE_DIR = Path(__file__).resolve().parents[2]

FAILURE_MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "predictive_maintenance"
    / "saved_models"
    / "random_forest_failure_model.joblib"
)

ANOMALY_MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "anomaly_detection"
    / "saved_models"
    / "isolation_forest.joblib"
)

TEST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "test.csv"
)


# -------------------------
# Load failure model
# -------------------------

failure_package = joblib.load(FAILURE_MODEL_FILE)

failure_model = failure_package["model"]
threshold = failure_package["threshold"]
failure_features = failure_package["features"]


# -------------------------
# Load anomaly model
# -------------------------

anomaly_model = joblib.load(ANOMALY_MODEL_FILE)

anomaly_features = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# -------------------------
# Load real unseen test data
# -------------------------

df = pd.read_csv(TEST_FILE)

# Select the same real unseen test sample used in XAI validation
sample = df.iloc[[35]]


# -------------------------
# Failure-risk prediction
# -------------------------

X_failure = sample[failure_features]

risk_probability = float(
    failure_model.predict_proba(X_failure)[0, 1]
)

if risk_probability >= 0.70:
    risk_level = "Critical"
elif risk_probability >= threshold:
    risk_level = "Warning"
else:
    risk_level = "Normal"


# -------------------------
# Anomaly prediction
# -------------------------

X_anomaly = sample[anomaly_features]

anomaly_prediction = anomaly_model.predict(X_anomaly)[0]

anomaly_detected = anomaly_prediction == -1

anomaly_score = float(
    -anomaly_model.decision_function(X_anomaly)[0]
)


# -------------------------
# Sensor data
# -------------------------

sensor_data = {
    "Air temperature [K]": float(
        sample["numerical__Air temperature [K]"].iloc[0]
    ),
    "Process temperature [K]": float(
        sample["numerical__Process temperature [K]"].iloc[0]
    ),
    "Rotational speed [rpm]": float(
        sample["numerical__Rotational speed [rpm]"].iloc[0]
    ),
    "Torque [Nm]": float(
        sample["numerical__Torque [Nm]"].iloc[0]
    ),
    "Tool wear [min]": float(
        sample["numerical__Tool wear [min]"].iloc[0]
    )
}


# -------------------------
# Recommendation service
# -------------------------

service = RecommendationService()

result = service.generate_recommendations(
    risk_level=risk_level,
    sensor_data=sensor_data,
    anomaly_detected=anomaly_detected,
    anomaly_score=anomaly_score
)


# -------------------------
# Results
# -------------------------

print("=== REAL MODEL RECOMMENDATION TEST ===")

print("Test sample index: 35")
print(
    f"Actual failure: "
    f"{int(sample['Machine failure'].iloc[0])}"
)
print(f"Failure risk: {risk_probability:.4f}")
print(f"Risk level: {risk_level}")
print(f"Anomaly detected: {anomaly_detected}")
print(f"Anomaly score: {anomaly_score:.4f}")

print("\n=== MAINTENANCE ACTIONS ===")

for item in result["maintenance_actions"]:
    print(f"- {item}")

print("\n=== SENSOR RECOMMENDATIONS ===")

for item in result["sensor_recommendations"]:
    print(f"- {item}")

print("\n=== ANOMALY RECOMMENDATIONS ===")

for item in result["anomaly_recommendations"]:
    print(f"- {item}")

print("\nFINAL RESULT")
print("Real model recommendation test completed successfully.")