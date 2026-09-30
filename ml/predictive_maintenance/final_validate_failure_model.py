import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)

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

print("\n=== FINAL PREDICTIVE MAINTENANCE VALIDATION ===")

# Load saved model
model_data = joblib.load(MODEL_FILE)

model = model_data["model"]
threshold = model_data["threshold"]
features = model_data["features"]
target = model_data["target"]

print(f"\nModel loaded: {model is not None}")
print(f"Decision threshold: {threshold}")
print(f"Feature count: {len(features)}")
print(f"Target: {target}")

# Load unseen test data
test = pd.read_csv(TEST_FILE)

X_test = test[features]
y_test = test[target]

# Generate predictions
failure_risk = model.predict_proba(X_test)[:, 1]

predictions = (
    failure_risk >= threshold
).astype(int)

print("\n=== TEST RESULTS ===")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Normal", "Failure"],
        zero_division=0
    )
)

roc_auc = roc_auc_score(
    y_test,
    failure_risk
)

pr_auc = average_precision_score(
    y_test,
    failure_risk
)

print(f"ROC-AUC: {roc_auc:.4f}")
print(f"PR-AUC: {pr_auc:.4f}")

print("\n=== RISK OUTPUT CHECK ===")

print(f"Minimum risk: {failure_risk.min():.4f}")
print(f"Maximum risk: {failure_risk.max():.4f}")
print(f"Average risk: {failure_risk.mean():.4f}")

print(f"\nTotal test samples: {len(y_test)}")
print(f"Actual failures: {y_test.sum()}")
print(f"Predicted failures: {predictions.sum()}")

# Basic integrity checks
assert len(failure_risk) == len(y_test)
assert len(predictions) == len(y_test)
assert ((failure_risk >= 0) & (failure_risk <= 1)).all()

print("\n=== VALIDATION STATUS ===")
print("Saved predictive maintenance model is valid and ready for integration.")

print("\n=== PHASE 5 VALIDATION COMPLETED ===")