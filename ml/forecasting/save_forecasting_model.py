import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "temperature_train.csv"
)

MODEL_DIR = BASE_DIR / "ml" / "forecasting" / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "temperature_forecasting_model.joblib"

df = pd.read_csv(TRAIN_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])

lag_steps = [1, 2, 3, 6, 12]

for lag in lag_steps:
    df[f"lag_{lag}"] = df["temperature"].shift(lag)

df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_6",
    "lag_12",
    "hour",
    "day_of_week",
]

df = df.dropna(subset=features)

X = df[features]
y = df["temperature"]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

model_package = {
    "model": model,
    "features": features,
    "target": "temperature",
    "target_unit": "celsius",
    "frequency": "20 minutes",
    "lag_steps": lag_steps,
    "baseline_mae": 5.5964,
    "baseline_rmse": 6.8407,
    "validated_mae": 3.8896,
    "validated_rmse": 4.8093,
}

joblib.dump(model_package, MODEL_FILE)

# Verify that the saved model can be loaded.
loaded_package = joblib.load(MODEL_FILE)

print("=== FORECASTING MODEL SAVED ===")
print(f"Model file: {MODEL_FILE}")
print(f"File exists: {MODEL_FILE.exists()}")
print(f"Features: {len(loaded_package['features'])}")
print(f"Target: {loaded_package['target']}")
print(f"Frequency: {loaded_package['frequency']}")
print(f"Validated MAE: {loaded_package['validated_mae']} °C")
print(f"Validated RMSE: {loaded_package['validated_rmse']} °C")

if MODEL_FILE.exists() and loaded_package["model"] is not None:
    print("\nFINAL RESULT")
    print("Forecasting model saved and successfully reloaded!")

print("\n=== PHASE 6 COMPLETED ===")