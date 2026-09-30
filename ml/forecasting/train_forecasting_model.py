import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "temperature_train.csv"
)

TEST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "temperature_test.csv"
)

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

train_df["timestamp"] = pd.to_datetime(train_df["timestamp"])
test_df["timestamp"] = pd.to_datetime(test_df["timestamp"])

# Combine only to create historical lag values.
# The model is trained only on the training portion.
combined = pd.concat([train_df, test_df], ignore_index=True)

lag_steps = [1, 2, 3, 6, 12]

for lag in lag_steps:
    combined[f"lag_{lag}"] = combined["temperature"].shift(lag)

# Time-based features
combined["hour"] = combined["timestamp"].dt.hour
combined["day_of_week"] = combined["timestamp"].dt.dayofweek

feature_columns = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_6",
    "lag_12",
    "hour",
    "day_of_week",
]

# Training section
train_part = combined.iloc[:len(train_df)].copy()
train_part = train_part.dropna(subset=feature_columns)

X_train = train_part[feature_columns]
y_train = train_part["temperature"]

# Testing section
test_part = combined.iloc[len(train_df):].copy()
test_part = test_part.dropna(subset=feature_columns)

X_test = test_part[feature_columns]
y_test = test_part["temperature"]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("=== RANDOM FOREST FORECASTING MODEL ===")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print(f"Features: {len(feature_columns)}")

print("\n=== MODEL SETTINGS ===")
print("Estimators: 200")
print("Maximum depth: 10")
print("Minimum samples per leaf: 3")

print("\n=== EVALUATION ===")
print(f"MAE:  {mae:.4f} °C")
print(f"RMSE: {rmse:.4f} °C")

print("\n=== BASELINE COMPARISON ===")
print("Baseline MAE:  5.5964 °C")
print("Baseline RMSE: 6.8407 °C")

print("\n=== SAMPLE PREDICTIONS ===")

results = test_part[["timestamp", "temperature"]].copy()
results["prediction"] = predictions

print(results.head(10).to_string(index=False))

print("\n=== FORECASTING MODEL TRAINING COMPLETED ===")