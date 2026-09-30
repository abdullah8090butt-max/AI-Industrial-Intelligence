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

combined = pd.concat([train_df, test_df], ignore_index=True)

lag_steps = [1, 2, 3, 6, 12]

for lag in lag_steps:
    combined[f"lag_{lag}"] = combined["temperature"].shift(lag)

combined["hour"] = combined["timestamp"].dt.hour
combined["day_of_week"] = combined["timestamp"].dt.dayofweek

features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_6",
    "lag_12",
    "hour",
    "day_of_week",
]

train_part = combined.iloc[:len(train_df)].dropna(subset=features)
test_part = combined.iloc[len(train_df):].dropna(subset=features)

X_train = train_part[features]
y_train = train_part["temperature"]

X_test = test_part[features]
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

baseline_mae = 5.5964
baseline_rmse = 6.8407

mae_improvement = ((baseline_mae - mae) / baseline_mae) * 100
rmse_improvement = ((baseline_rmse - rmse) / baseline_rmse) * 100

print("=== FINAL FORECASTING VALIDATION ===")

print(f"Test samples: {len(X_test)}")
print(f"Actual values: {len(y_test)}")
print(f"Predictions: {len(predictions)}")

print("\n=== MODEL PERFORMANCE ===")
print(f"MAE:  {mae:.4f} °C")
print(f"RMSE: {rmse:.4f} °C")

print("\n=== BASELINE IMPROVEMENT ===")
print(f"MAE improvement:  {mae_improvement:.2f}%")
print(f"RMSE improvement: {rmse_improvement:.2f}%")

print("\n=== PREDICTION VALIDATION ===")
print(f"NaN predictions: {np.isnan(predictions).sum()}")
print(f"Minimum prediction: {predictions.min():.3f} °C")
print(f"Maximum prediction: {predictions.max():.3f} °C")

print("\n=== ACTUAL RANGE ===")
print(f"Minimum actual: {y_test.min():.3f} °C")
print(f"Maximum actual: {y_test.max():.3f} °C")

if (
    len(predictions) == len(y_test)
    and not np.isnan(predictions).any()
    and mae < baseline_mae
    and rmse < baseline_rmse
):
    print("\nFINAL RESULT")
    print("Forecasting model passed validation!")
else:
    print("\nFINAL RESULT")
    print("Forecasting model requires further investigation.")

print("\n=== VALIDATION COMPLETED ===")