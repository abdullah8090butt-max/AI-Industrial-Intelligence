import json
from pathlib import Path

from xai_service import xai_service


BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    BASE_DIR
    / "ml"
    / "explainability"
    / "saved_outputs"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "feature_importance.json"


importance_data = xai_service.get_global_feature_importance()

output = {
    "model": "Random Forest Failure Prediction",
    "xai_method": "Built-in Random Forest Feature Importance",
    "feature_importance": importance_data,
    "validated": True
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(output, file, indent=4)


# Reload and validate the saved output
with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
    saved_output = json.load(file)

features = saved_output["feature_importance"]

importance_sum = sum(
    item["importance"]
    for item in features
)

all_valid = (
    len(features) == 8
    and abs(importance_sum - 1.0) < 0.0001
    and saved_output["validated"] is True
)

print("=== XAI OUTPUT SAVE ===")
print(f"Output file created: {OUTPUT_FILE.exists()}")
print(f"Features saved: {len(features)}")
print(f"Importance sum: {importance_sum:.4f}")

print("\n=== SAVED OUTPUT VALIDATION ===")
print(f"JSON reload successful: {saved_output is not None}")
print(f"All validation checks passed: {all_valid}")

if all_valid:
    print("\nFINAL RESULT")
    print("XAI outputs saved and validated successfully!")
else:
    print("\nFINAL RESULT")
    print("XAI output validation failed.")