import pandas as pd
import joblib
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "anomaly_detection"
    / "saved_models"
    / "isolation_forest.joblib"
)


# Load saved model
model = joblib.load(MODEL_PATH)


# Load test data
test = pd.read_csv(PROCESSED_DIR / "test.csv")


# Sensor features
SENSOR_FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# Generate predictions
predictions = model.predict(test[SENSOR_FEATURES])

anomalies = (predictions == -1).sum()


print("\n=== FINAL ANOMALY MODEL VALIDATION ===")

print(f"Model loaded: {MODEL_PATH.exists()}")
print(f"Test samples: {len(test)}")
print(f"Detected anomalies: {anomalies}")

print(f"Model contamination: {model.contamination}")

if len(predictions) == len(test) and anomalies > 0:
    print("\nFinal anomaly model is ready for integration!")
else:
    print("\nValidation failed. Check the model and test data.")

print("\n=== PHASE 4 VALIDATION COMPLETED ===")