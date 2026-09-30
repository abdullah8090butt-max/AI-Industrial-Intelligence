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

TEST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "test.csv"
)

package = joblib.load(MODEL_FILE)

model = package["model"]
features = package["features"]
threshold = package["threshold"]

df = pd.read_csv(TEST_FILE)

X_test = df[features]
y_test = df["Machine failure"]

# Select the highest-risk unseen test sample.
risk_probabilities = model.predict_proba(X_test)[:, 1]
sample_index = risk_probabilities.argmax()

sample = X_test.iloc[sample_index]
actual = int(y_test.iloc[sample_index])
risk = float(risk_probabilities[sample_index])

if risk >= 0.70:
    risk_level = "Critical"
elif risk >= threshold:
    risk_level = "Warning"
else:
    risk_level = "Normal"

importance_df = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    "importance",
    ascending=False
)

print("=== INDIVIDUAL XAI EXPLANATION ===")

print(f"Test sample index: {sample_index}")
print(f"Actual failure: {actual}")
print(f"Predicted failure risk: {risk:.4f}")
print(f"Risk percentage: {risk * 100:.2f}%")
print(f"Risk level: {risk_level}")

print("\n=== MACHINE FEATURE VALUES ===")

for feature in features:
    print(f"{feature}: {sample[feature]:.4f}")

print("\n=== FEATURE IMPORTANCE CONTEXT ===")

for _, row in importance_df.iterrows():
    feature = row["feature"]
    importance = row["importance"]

    print(
        f"{feature}: "
        f"importance={importance:.4f} "
        f"({importance * 100:.2f}%)"
    )

print("\n=== INDIVIDUAL EXPLANATION COMPLETED ===")