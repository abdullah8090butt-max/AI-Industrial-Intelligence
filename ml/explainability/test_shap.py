import pandas as pd
import joblib
import shap
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "predictive_maintenance"
    / "saved_models"
    / "random_forest_failure_model.joblib"
)

TEST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "test.csv"
)

package = joblib.load(MODEL_FILE)

model = package["model"]
features = package["features"]

df = pd.read_csv(TEST_FILE)

X_test = df[features]

# Use a small sample for the compatibility test.
X_sample = X_test.iloc[:100]

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

print("=== SHAP COMPATIBILITY TEST ===")
print(f"Model loaded: {model is not None}")
print(f"Features: {len(features)}")
print(f"Samples explained: {len(X_sample)}")

if isinstance(shap_values, list):
    print(f"SHAP output type: list")
    print(f"Number of outputs: {len(shap_values)}")
    for i, values in enumerate(shap_values):
        print(f"Output {i} shape: {values.shape}")
else:
    print(f"SHAP output type: {type(shap_values).__name__}")
    print(f"SHAP shape: {shap_values.shape}")

print("\n=== SHAP TEST COMPLETED ===")