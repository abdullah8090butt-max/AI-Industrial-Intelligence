import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = BASE_DIR / "data" / "processed" / "ai4i_processed.csv"


# Load processed dataset
df = pd.read_csv(DATA_FILE)


print("\n=== DATASET OVERVIEW ===")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# --------------------------------------------------
# 1. Sensor statistics
# --------------------------------------------------

sensor_features = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

print("\n=== SENSOR STATISTICS ===")
print(df[sensor_features].describe())


# --------------------------------------------------
# 2. Correlation analysis
# --------------------------------------------------

print("\n=== SENSOR CORRELATION ===")
print(df[sensor_features].corr().round(2))

plt.figure(figsize=(10, 7))

sns.heatmap(
    df[sensor_features].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Sensor Correlation Matrix")
plt.tight_layout()
plt.show()


# --------------------------------------------------
# 3. Failure distribution
# --------------------------------------------------

print("\n=== MACHINE FAILURE ===")
print(df["Machine failure"].value_counts())

print("\n=== FAILURE PERCENTAGE ===")
print(
    (df["Machine failure"].value_counts(normalize=True) * 100)
    .round(2)
)


# --------------------------------------------------
# 4. Sensor values vs failure
# --------------------------------------------------

for feature in sensor_features:

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Machine failure",
        y=feature
    )

    plt.title(f"{feature} vs Machine Failure")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# 5. Failure type distribution
# --------------------------------------------------

failure_types = ["TWF", "HDF", "PWF", "OSF", "RNF"]

failure_counts = df[failure_types].sum().sort_values(ascending=False)

print("\n=== FAILURE TYPE COUNTS ===")
print(failure_counts)

plt.figure(figsize=(8, 5))

failure_counts.plot(kind="bar")

plt.title("Failure Type Distribution")
plt.xlabel("Failure Type")
plt.ylabel("Number of Records")

plt.tight_layout()
plt.show()


print("\n=== EDA COMPLETED ===")