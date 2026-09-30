import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

train = pd.read_csv(PROCESSED_DIR / "train.csv")
test = pd.read_csv(PROCESSED_DIR / "test.csv")

FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]",
    "categorical__Type_0",
    "categorical__Type_1",
    "categorical__Type_2"
]

TARGET = "Machine failure"
THRESHOLD = 0.40

X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

failure_probabilities = model.predict_proba(X_test)[:, 1]

predictions = (
    failure_probabilities >= THRESHOLD
).astype(int)

print("\n=== FINAL UNSEEN TEST EVALUATION ===")

print(f"\nDecision Threshold: {THRESHOLD:.2f}")

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

print(
    f"ROC-AUC: "
    f"{roc_auc_score(y_test, failure_probabilities):.4f}"
)

print(
    f"PR-AUC: "
    f"{average_precision_score(y_test, failure_probabilities):.4f}"
)

print("\n=== TEST SET SUMMARY ===")
print(f"Total test samples: {len(y_test)}")
print(f"Actual failures: {y_test.sum()}")
print(f"Predicted failures: {predictions.sum()}")

print("\n=== FINAL TEST VALIDATION COMPLETED ===")