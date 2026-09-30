import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Load datasets
train = pd.read_csv(PROCESSED_DIR / "train.csv")
validation = pd.read_csv(PROCESSED_DIR / "validation.csv")
test = pd.read_csv(PROCESSED_DIR / "test.csv")


# Feature columns
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


# Separate features and target
X_train = train[FEATURES]
y_train = train[TARGET]

X_validation = validation[FEATURES]
y_validation = validation[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]


print("\n=== FAILURE PREDICTION DATA ===")

print(f"Training:   X={X_train.shape}, y={y_train.shape}")
print(f"Validation: X={X_validation.shape}, y={y_validation.shape}")
print(f"Test:       X={X_test.shape}, y={y_test.shape}")

print("\nFailure counts:")
print(f"Train:       {y_train.sum()}")
print(f"Validation:  {y_validation.sum()}")
print(f"Test:        {y_test.sum()}")

print("\nFeature count:", len(FEATURES))
print("Target:", TARGET)

print("\n=== FAILURE DATA PREPARATION COMPLETED ===")