import joblib
import pandas as pd
from pathlib import Path

from ml.simulator.sensor_generator import generate_sensor_reading


# ============================================================
# Project Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FAILURE_MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "predictive_maintenance"
    / "saved_models"
    / "random_forest_failure_model.joblib"
)

PREPROCESSOR_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "preprocessor.joblib"
)


# ============================================================
# Required Model Features
# ============================================================

NUMERICAL_FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]


# ============================================================
# Load Model
# ============================================================

failure_package = joblib.load(
    FAILURE_MODEL_FILE
)

failure_model = failure_package["model"]

threshold = float(
    failure_package["threshold"]
)

failure_features = failure_package["features"]

preprocessor = joblib.load(
    PREPROCESSOR_FILE
)


# ============================================================
# Predict Failure Risk
# ============================================================

def predict_failure_risk(
    sensor_data: dict,
    machine_type: str = "M"
) -> dict:

    row = {
        "Air temperature [K]":
            float(sensor_data["Air temperature [K]"]),

        "Process temperature [K]":
            float(sensor_data["Process temperature [K]"]),

        "Rotational speed [rpm]":
            float(sensor_data["Rotational speed [rpm]"]),

        "Torque [Nm]":
            float(sensor_data["Torque [Nm]"]),

        "Tool wear [min]":
            float(sensor_data["Tool wear [min]"]),

        "Type": machine_type
    }

    raw_df = pd.DataFrame([row])

    # Transform raw simulator data using
    # the same preprocessing pipeline used during training.
    X_transformed = preprocessor.transform(
        raw_df
    )

    X_model = pd.DataFrame(
        X_transformed,
        columns=failure_features
    )

    risk_probability = float(
        failure_model.predict_proba(
            X_model
        )[0, 1]
    )

    predicted_failure = bool(
        risk_probability >= threshold
    )

    if risk_probability >= 0.70:
        risk_level = "Critical"
    elif risk_probability >= threshold:
        risk_level = "Warning"
    else:
        risk_level = "Normal"

    return {
        "failure_risk": round(
            risk_probability,
            4
        ),
        "predicted_failure": predicted_failure,
        "risk_level": risk_level,
        "threshold": threshold
    }


# ============================================================
# Validation
# ============================================================

if __name__ == "__main__":

    print("=== FAILURE-RISK MODEL TEST ===")

    all_valid = True

    for scenario_name in [
        "Normal",
        "Warning",
        "Critical"
    ]:

        sensor_data = generate_sensor_reading(
            scenario_name,
            seed=42
        )

        result = predict_failure_risk(
            sensor_data
        )

        print(f"\n--- {scenario_name} ---")

        print(
            f"Failure risk: "
            f"{result['failure_risk']:.4f}"
        )

        print(
            f"Predicted failure: "
            f"{result['predicted_failure']}"
        )

        print(
            f"Risk level: "
            f"{result['risk_level']}"
        )

        print(
            f"Threshold: "
            f"{result['threshold']:.2f}"
        )

        if not (
            0.0 <= result["failure_risk"] <= 1.0
        ):
            all_valid = False

        if result["risk_level"] not in [
            "Normal",
            "Warning",
            "Critical"
        ]:
            all_valid = False

        if not isinstance(
            result["predicted_failure"],
            bool
        ):
            all_valid = False

    print("\n=== MODEL CONNECTION VALIDATION ===")

    print(
        f"Model file available: "
        f"{FAILURE_MODEL_FILE.exists()}"
    )

    print(
        f"Preprocessor available: "
        f"{PREPROCESSOR_FILE.exists()}"
    )

    print(
        f"Required features loaded: "
        f"{len(failure_features)}"
    )

    print(
        f"All predictions valid: "
        f"{all_valid}"
    )

    if all_valid:
        print(
            "\nStep 9.4 completed successfully!"
        )
    else:
        print(
            "\nStep 9.4 validation failed."
        )