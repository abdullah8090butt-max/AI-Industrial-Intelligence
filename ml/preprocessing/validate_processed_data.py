import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Files
train_file = PROCESSED_DIR / "train.csv"
validation_file = PROCESSED_DIR / "validation.csv"
test_file = PROCESSED_DIR / "test.csv"


# Load datasets
train = pd.read_csv(train_file)
validation = pd.read_csv(validation_file)
test = pd.read_csv(test_file)


datasets = {
    "Train": train,
    "Validation": validation,
    "Test": test
}


print("\n=== PROCESSED DATA VALIDATION ===")


for name, data in datasets.items():

    print(f"\n--- {name} ---")

    print(f"Shape: {data.shape}")

    print(f"Missing values: {data.isnull().sum().sum()}")

    print(
        "Target distribution:"
    )

    print(
        data["Machine failure"].value_counts().to_dict()
    )


# --------------------------------------------------
# Feature validation
# --------------------------------------------------

expected_features = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]",
    "categorical__Type_0",
    "categorical__Type_1",
    "categorical__Type_2"
]

expected_columns = expected_features + ["Machine failure"]


print("\n=== COLUMN VALIDATION ===")

print(
    "Columns correct:",
    list(train.columns) == expected_columns
)


# --------------------------------------------------
# Final validation
# --------------------------------------------------

all_valid = True

for name, data in datasets.items():

    if data.isnull().sum().sum() != 0:
        all_valid = False

    if data.shape[1] != 9:
        all_valid = False

    if set(data["Machine failure"].unique()) != {0, 1}:
        all_valid = False


print("\n=== FINAL RESULT ===")

if all_valid:
    print("Processed datasets are valid!")
else:
    print("Validation failed. Check the output above.")


print("\n=== VALIDATION COMPLETED ===")