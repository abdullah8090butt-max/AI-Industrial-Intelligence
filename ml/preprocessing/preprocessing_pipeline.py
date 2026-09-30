import pandas as pd
import joblib
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "processed" / "ai4i_processed.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

PIPELINE_FILE = OUTPUT_DIR / "preprocessor.joblib"


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
# Train / validation / test split
# --------------------------------------------------

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    stratify=y,
    random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=42
)


# --------------------------------------------------
# Preprocessing pipeline
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            NUMERICAL_FEATURES
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            CATEGORICAL_FEATURES
        )
    ]
)


# --------------------------------------------------
# Fit only on training data
# --------------------------------------------------

X_train_processed = preprocessor.fit_transform(X_train)
X_val_processed = preprocessor.transform(X_val)
X_test_processed = preprocessor.transform(X_test)


# --------------------------------------------------
# Convert processed features to DataFrames
# --------------------------------------------------

feature_names = preprocessor.get_feature_names_out()

X_train_df = pd.DataFrame(
    X_train_processed,
    columns=feature_names,
    index=X_train.index
)

X_val_df = pd.DataFrame(
    X_val_processed,
    columns=feature_names,
    index=X_val.index
)

X_test_df = pd.DataFrame(
    X_test_processed,
    columns=feature_names,
    index=X_test.index
)


# Add target column
X_train_df[TARGET] = y_train.values
X_val_df[TARGET] = y_val.values
X_test_df[TARGET] = y_test.values


# --------------------------------------------------
# Save processed datasets
# --------------------------------------------------

train_file = OUTPUT_DIR / "train.csv"
validation_file = OUTPUT_DIR / "validation.csv"
test_file = OUTPUT_DIR / "test.csv"

X_train_df.to_csv(train_file, index=False)
X_val_df.to_csv(validation_file, index=False)
X_test_df.to_csv(test_file, index=False)


# --------------------------------------------------
# Save preprocessing pipeline
# --------------------------------------------------

joblib.dump(preprocessor, PIPELINE_FILE)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n=== PROCESSED DATA SAVED ===")

print(f"Training:   {train_file}")
print(f"Validation: {validation_file}")
print(f"Test:       {test_file}")

print(f"\nPreprocessor: {PIPELINE_FILE}")

print("\nShapes:")
print(f"Train:      {X_train_df.shape}")
print(f"Validation: {X_val_df.shape}")
print(f"Test:       {X_test_df.shape}")

print("\n=== STEP 3.8 COMPLETED ===")