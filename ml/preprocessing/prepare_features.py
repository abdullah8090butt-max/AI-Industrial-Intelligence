import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "processed" / "ai4i_processed.csv"


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)


# --------------------------------------------------
# Features and target
# --------------------------------------------------

NUMERICAL_FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

CATEGORICAL_FEATURES = [
    "Type"
]

TARGET = "Machine failure"


X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
y = df[TARGET]


# --------------------------------------------------
# First split: 70% train, 30% temporary
# --------------------------------------------------

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    stratify=y,
    random_state=42
)


# --------------------------------------------------
# Second split: 15% validation, 15% test
# --------------------------------------------------

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=42
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n=== DATA SPLIT RESULTS ===")

print(f"Training samples:   {len(X_train)}")
print(f"Validation samples: {len(X_val)}")
print(f"Test samples:       {len(X_test)}")


print("\n=== TRAIN FAILURE DISTRIBUTION ===")
print(y_train.value_counts())

print("\n=== VALIDATION FAILURE DISTRIBUTION ===")
print(y_val.value_counts())

print("\n=== TEST FAILURE DISTRIBUTION ===")
print(y_test.value_counts())


print("\n=== FAILURE PERCENTAGES ===")

print(
    "Train:",
    (y_train.mean() * 100).round(2),
    "%"
)

print(
    "Validation:",
    (y_val.mean() * 100).round(2),
    "%"
)

print(
    "Test:",
    (y_test.mean() * 100).round(2),
    "%"
)


print("\n=== DATA SPLITTING COMPLETED ===")