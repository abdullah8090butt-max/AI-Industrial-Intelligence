import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "raw" / "time_series" / "telemetry_readings.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "forecasting"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Select temperature readings
temperature_df = df[df["metric_type"] == "temperature"].copy()

# Sort chronologically
temperature_df = temperature_df.sort_values("timestamp")

# Keep only required columns
temperature_df = temperature_df[["timestamp", "value"]]

# Rename target column
temperature_df = temperature_df.rename(columns={"value": "temperature"})

# Chronological 80/20 split
split_index = int(len(temperature_df) * 0.80)

train_df = temperature_df.iloc[:split_index].copy()
test_df = temperature_df.iloc[split_index:].copy()

train_file = OUTPUT_DIR / "temperature_train.csv"
test_file = OUTPUT_DIR / "temperature_test.csv"

train_df.to_csv(train_file, index=False)
test_df.to_csv(test_file, index=False)

print("=== FORECASTING DATA PREPARATION ===")
print(f"Total temperature readings: {len(temperature_df)}")
print(f"Training readings: {len(train_df)}")
print(f"Testing readings: {len(test_df)}")

print("\n=== TRAINING PERIOD ===")
print(f"Start: {train_df['timestamp'].min()}")
print(f"End:   {train_df['timestamp'].max()}")

print("\n=== TESTING PERIOD ===")
print(f"Start: {test_df['timestamp'].min()}")
print(f"End:   {test_df['timestamp'].max()}")

print("\n=== MISSING VALUES ===")
print(f"Train: {train_df.isnull().sum().sum()}")
print(f"Test:  {test_df.isnull().sum().sum()}")

print("\n=== FILES SAVED ===")
print(train_file)
print(test_file)

print("\n=== FORECASTING DATA PREPARATION COMPLETED ===")