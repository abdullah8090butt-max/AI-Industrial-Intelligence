import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "predictive_maintenance"
    / "saved_models"
    / "random_forest_failure_model.joblib"
)

TEST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "test.csv"
)

package = joblib.load(MODEL_FILE)

model = package["model"]
features = package["features"]
threshold = package["threshold"]

df = pd.read_csv(TEST_FILE)

X_test = df[features]

# Feature importance validation
importances = model.feature_importances_

importance_sum = importances.sum()
importance_count = len(importances)

# Risk validation
risk_probabilities = model.predict_proba(X_test)[:, 1]

sample_index = risk_probabilities.argmax()
risk = float(risk_probabilities[sample_index])

if risk >= 0.70:
    risk_level = "Critical"
elif risk >= threshold:
    risk_level = "Warning"
else:
    risk_level = "Normal"

print("=== XAI VALIDATION ===")

print(f"Model loaded: {model is not None}")
print(f"Features expected: {len(features)}")
print(f"Feature importances: {importance_count}")

print("\n=== IMPORTANCE VALIDATION ===")
print(f"Importance sum: {importance_sum:.4f}")
print(f"All importances >= 0: {(importances >= 0).all()}")

print("\n=== RISK VALIDATION ===")
print(f"Risk probability: {risk:.4f}")
print(f"Risk range valid: {0 <= risk <= 1}")
print(f"Risk level: {risk_level}")

print("\n=== FEATURE COVERAGE ===")
for feature in features:
    print(f"{feature}: present")

all_valid = (
    len(features) == 8
    and importance_count == 8
    and abs(importance_sum - 1.0) < 0.0001
    and (importances >= 0).all()
    and 0 <= risk <= 1
)

if all_valid:
    print("\nFINAL RESULT")
    print("XAI validation passed!")
else:
    print("\nFINAL RESULT")
    print("XAI validation failed.")

print("\n=== VALIDATION COMPLETED ===")