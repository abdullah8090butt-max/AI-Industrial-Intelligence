import pandas as pd

file_path = "../data/raw/ai4i_2020/ai4i2020.csv"

df = pd.read_csv(file_path)

print("=== MACHINE FAILURE DISTRIBUTION ===")
print(df["Machine failure"].value_counts())

print("\n=== FAILURE PERCENTAGE ===")
print(df["Machine failure"].value_counts(normalize=True) * 100)

print("\n=== FAILURE TYPES ===")
failure_columns = ["TWF", "HDF", "PWF", "OSF", "RNF"]

for column in failure_columns:
    print(f"\n{column}:")
    print(df[column].value_counts())

print("\n=== SENSOR STATISTICS ===")
sensor_columns = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

print(df[sensor_columns].describe())