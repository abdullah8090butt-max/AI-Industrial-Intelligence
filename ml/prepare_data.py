import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "raw" / "ai4i_2020" / "ai4i2020.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "ai4i_processed.csv"


# Load dataset
df = pd.read_csv(INPUT_FILE)

# Remove identifier columns
df = df.drop(columns=["UDI", "Product ID"])

# Convert machine type to numerical representation
df["Type"] = df["Type"].map({
    "L": 0,
    "M": 1,
    "H": 2
})

# Create processed-data directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Save processed dataset
df.to_csv(OUTPUT_FILE, index=False)

print("Dataset preparation completed.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {OUTPUT_FILE}")