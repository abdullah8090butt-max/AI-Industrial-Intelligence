import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Load datasets
train = pd.read_csv(PROCESSED_DIR / "train.csv")
validation = pd.read_csv(PROCESSED_DIR / "validation.csv")


# Features
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


X_train = train[FEATURES]
y_train = train[TARGET]

X_validation = validation[FEATURES]
y_validation = validation[TARGET]


# Train Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# Predictions and probabilities
predictions = model.predict(X_validation)
failure_probabilities = model.predict_proba(X_validation)[:, 1]


print("\n=== FAILURE MODEL EVALUATION ===")

print("\nConfusion Matrix:")
print(confusion_matrix(y_validation, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_validation,
        predictions,
        target_names=["Normal", "Failure"],
        zero_division=0
    )
)

print(
    f"ROC-AUC: "
    f"{roc_auc_score(y_validation, failure_probabilities):.4f}"
)


print("\n=== FAILURE RISK DISTRIBUTION ===")

print(
    pd.Series(failure_probabilities).describe()
)


print("\nHighest-risk validation records:")

top_indices = failure_probabilities.argsort()[-10:][::-1]

for index in top_indices:
    print(
        f"Validation index: {index} | "
        f"Failure risk: {failure_probabilities[index] * 100:.2f}% | "
        f"Actual failure: {y_validation.iloc[index]}"
    )


print("\n=== EVALUATION COMPLETED ===")