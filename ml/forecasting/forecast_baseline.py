import pandas as pd
import numpy as np
from pathlib import Path
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

# Persistence baseline:
# predict each test value using the previous observed value.
combined = pd.concat([train_df, test_df], ignore_index=True)

combined["prediction"] = combined["temperature"].shift(1)

test_predictions = combined.iloc[len(train_df):].copy()

# First test prediction uses the final training temperature.
test_predictions = test_predictions.dropna(subset=["prediction"])

actual = test_predictions["temperature"].values
predicted = test_predictions["prediction"].values

mae = mean_absolute_error(actual, predicted)
rmse = np.sqrt(mean_squared_error(actual, predicted))

print("=== FORECASTING BASELINE ===")
print(f"Training readings: {len(train_df)}")
print(f"Testing readings: {len(test_predictions)}")

print("\n=== BASELINE MODEL ===")
print("Method: Persistence")
print("Prediction: Previous observed temperature")

print("\n=== EVALUATION ===")
print(f"MAE:  {mae:.4f} °C")
print(f"RMSE: {rmse:.4f} °C")

print("\n=== SAMPLE PREDICTIONS ===")
print(
    test_predictions[
        ["timestamp", "temperature", "prediction"]
    ].head(10).to_string(index=False)
)

print("\n=== BASELINE COMPLETED ===")