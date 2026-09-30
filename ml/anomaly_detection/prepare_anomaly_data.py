import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Load processed datasets
train = pd.read_csv(PROCESSED_DIR / "train.csv")
validation = pd.read_csv(PROCESSED_DIR / "validation.csv")
test = pd.read_csv(PROCESSED_DIR / "test.csv")


# Sensor features only
SENSOR_FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# Select sensor data
X_train = train[SENSOR_FEATURES]
X_validation = validation[SENSOR_FEATURES]
X_test = test[SENSOR_FEATURES]


print("\n=== ANOMALY DETECTION DATA ===")

print(f"Training shape: {X_train.shape}")
print(f"Validation shape: {X_validation.shape}")
print(f"Test shape: {X_test.shape}")

print("\nSensor features:")
for feature in SENSOR_FEATURES:
    print(feature)

print("\nMissing values:")
print(
    "Train:",
    X_train.isnull().sum().sum()
)

print(
    "Validation:",
    X_validation.isnull().sum().sum()
)

print(
    "Test:",
    X_test.isnull().sum().sum()
)

print("\n=== ANOMALY DATA PREPARATION COMPLETED ===")