import json
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

PREPROCESSOR_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "preprocessor.joblib"
)

TEST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "test.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "ml"
    / "recommendations"
    / "saved_outputs"
)

OUTPUT_FILE = OUTPUT_DIR / "recommendation_output.json"


# ============================================================
# Load models
# ============================================================

failure_package = joblib.load(FAILURE_MODEL_FILE)

failure_model = failure_package["model"]
threshold = float(failure_package["threshold"])
failure_features = failure_package["features"]

anomaly_model = joblib.load(ANOMALY_MODEL_FILE)

preprocessor = joblib.load(PREPROCESSOR_FILE)


anomaly_features = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# ============================================================
# Load real test data
# ============================================================

df = pd.read_csv(TEST_FILE)

SAMPLE_INDEX = 35
sample = df.iloc[[SAMPLE_INDEX]]


# ============================================================
# Failure risk
# ============================================================

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


# ============================================================
# Anomaly detection
# ============================================================

X_anomaly = sample[anomaly_features]

anomaly_prediction = int(
    anomaly_model.predict(X_anomaly)[0]
)

anomaly_detected = bool(
    anomaly_prediction == -1
)

anomaly_score = float(
    -anomaly_model.decision_function(X_anomaly)[0]
)


# ============================================================
# Convert standardized values back to real sensor units
# ============================================================

X_processed = sample[anomaly_features].copy()

numerical_transformer = preprocessor.named_transformers_["numerical"]

raw_sensor_values = numerical_transformer.inverse_transform(
    X_processed
)

raw_sensor_values = raw_sensor_values[0]


sensor_data = {
    "Air temperature [K]": float(raw_sensor_values[0]),
    "Process temperature [K]": float(raw_sensor_values[1]),
    "Rotational speed [rpm]": float(raw_sensor_values[2]),
    "Torque [Nm]": float(raw_sensor_values[3]),
    "Tool wear [min]": float(raw_sensor_values[4])
}


# ============================================================
# Generate recommendations
# ============================================================

service = RecommendationService()

result = service.generate_recommendations(
    risk_level=risk_level,
    sensor_data=sensor_data,
    anomaly_detected=anomaly_detected,
    anomaly_score=anomaly_score
)


# ============================================================
# Prepare JSON-safe output
# ============================================================

output = {
    "test_sample_index": int(SAMPLE_INDEX),
    "actual_failure": int(
        sample["Machine failure"].iloc[0]
    ),
    "failure_risk": float(
        round(risk_probability, 4)
    ),
    "risk_level": str(risk_level),
    "anomaly_detected": bool(anomaly_detected),
    "anomaly_score": float(
        round(anomaly_score, 4)
    ),
    "sensor_data": {
        key: float(round(value, 3))
        for key, value in sensor_data.items()
    },
    "recommendations": result,
    "validated": True
}


# ============================================================
# Save JSON
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        output,
        file,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# Reload saved output
# ============================================================

with open(
    OUTPUT_FILE,
    "r",
    encoding="utf-8"
) as file:
    saved_output = json.load(file)


# ============================================================
# Validate
# ============================================================

all_valid = (
    saved_output["actual_failure"] in [0, 1]
    and 0 <= saved_output["failure_risk"] <= 1
    and saved_output["risk_level"] in [
        "Normal",
        "Warning",
        "Critical"
    ]
    and isinstance(
        saved_output["anomaly_detected"],
        bool
    )
    and isinstance(
        saved_output["anomaly_score"],
        (int, float)
    )
    and "sensor_data" in saved_output
    and "recommendations" in saved_output
    and saved_output["validated"] is True
)


# ============================================================
# Final output
# ============================================================

print("=== RECOMMENDATION OUTPUT SAVE ===")

print(
    f"Output file created: "
    f"{OUTPUT_FILE.exists()}"
)

print(
    f"Failure risk: "
    f"{saved_output['failure_risk']:.4f}"
)

print(
    f"Risk level: "
    f"{saved_output['risk_level']}"
)

print(
    f"Anomaly detected: "
    f"{saved_output['anomaly_detected']}"
)

print(
    f"Anomaly score: "
    f"{saved_output['anomaly_score']:.4f}"
)

print("\n=== RAW SENSOR VALUES ===")

for key, value in saved_output["sensor_data"].items():
    print(f"{key}: {value}")


print("\n=== SAVED OUTPUT VALIDATION ===")

print(
    f"JSON reload successful: "
    f"{saved_output is not None}"
)

print(
    f"All validation checks passed: "
    f"{all_valid}"
)


if all_valid:
    print("\nFINAL RESULT")
    print(
        "Recommendation outputs saved and "
        "validated successfully!"
    )
else:
    print("\nFINAL RESULT")
    print(
        "Recommendation output validation failed."
    )