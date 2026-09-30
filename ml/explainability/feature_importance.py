import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "predictive_maintenance"
    / "saved_models"
    / "random_forest_failure_model.joblib"
)

package = joblib.load(MODEL_FILE)

model = package["model"]
features = package["features"]

importances = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": features,
    "importance": importances
})

importance_df = importance_df.sort_values(
    "importance",
    ascending=False
).reset_index(drop=True)

print("=== GLOBAL XAI FEATURE IMPORTANCE ===")
print(f"Model loaded: {model is not None}")
print(f"Features analyzed: {len(features)}")

print("\n=== FEATURE RANKING ===")

for index, row in importance_df.iterrows():
    print(
        f"{index + 1}. "
        f"{row['feature']}: "
        f"{row['importance']:.4f}"
    )

print("\n=== IMPORTANCE TOTAL ===")
print(f"{importance_df['importance'].sum():.4f}")

print("\n=== XAI ANALYSIS COMPLETED ===")