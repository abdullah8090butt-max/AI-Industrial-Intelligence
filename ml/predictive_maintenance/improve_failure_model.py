import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

train = pd.read_csv(PROCESSED_DIR / "train.csv")
validation = pd.read_csv(PROCESSED_DIR / "validation.csv")

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

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

failure_probabilities = model.predict_proba(X_validation)[:, 1]

thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

print("\n=== FAILURE THRESHOLD ANALYSIS ===")

best_threshold = None
best_f1 = -1

for threshold in thresholds:
    predictions = (failure_probabilities >= threshold).astype(int)

    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_validation,
        predictions,
        zero_division=0
    )

    print(
        f"Threshold: {threshold:.2f} | "
        f"Precision: {precision:.2f} | "
        f"Recall: {recall:.2f} | "
        f"F1: {f1:.2f}"
    )

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

print("\n=== SELECTED THRESHOLD ===")
print(f"Threshold: {best_threshold:.2f}")
print(f"Validation F1: {best_f1:.2f}")

print("\n=== IMPROVEMENT COMPLETED ===")