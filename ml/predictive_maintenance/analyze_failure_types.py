import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "ai4i_2020"
    / "ai4i2020.csv"
)

df = pd.read_csv(INPUT_FILE)

FAILURE_TYPES = [
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF"
]

print("\n=== FAILURE TYPE ANALYSIS ===")

print("\nFailure Type Counts:")

for failure_type in FAILURE_TYPES:
    count = int(df[failure_type].sum())
    print(f"{failure_type}: {count}")

print("\nFailure Type Percentages:")

total_failures = df["Machine failure"].sum()

for failure_type in FAILURE_TYPES:
    count = df[failure_type].sum()

    percentage = (
        (count / total_failures) * 100
        if total_failures > 0
        else 0
    )

    print(
        f"{failure_type}: "
        f"{percentage:.2f}% of machine failures"
    )

print("\n=== FAILURE TYPE ANALYSIS COMPLETED ===")