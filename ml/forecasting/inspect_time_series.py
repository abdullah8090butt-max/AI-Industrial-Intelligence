import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "raw" / "time_series" / "telemetry_readings.csv"

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

print("=== TIME-SERIES VALIDATION ===")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\n=== TIME RANGE ===")
print(f"Start: {df['timestamp'].min()}")
print(f"End:   {df['timestamp'].max()}")

print("\n=== METRIC TYPES ===")
print(df["metric_type"].value_counts())

print("\n=== SENSOR TYPES ===")
print(df[["sensor_id", "metric_type", "unit"]].drop_duplicates().sort_values("sensor_id"))

print("\n=== MACHINE DISTRIBUTION ===")
print(df["machine_id"].value_counts())

print("\n=== STATUS DISTRIBUTION ===")
print(df["status"].value_counts())

print("\n=== ANOMALY FLAG ===")
print(df["anomaly_flag"].value_counts())

print("\n=== TIME DIFFERENCES ===")
time_diff = df["timestamp"].sort_values().diff().dropna()
print(time_diff.value_counts().head(10))

print("\n=== VALUE STATISTICS BY METRIC ===")
print(
    df.groupby("metric_type")["value"]
    .agg(["count", "mean", "min", "max"])
)

print("\n=== VALIDATION COMPLETED ===")