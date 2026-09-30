import joblib
import pandas as pd
from pathlib import Path

from ml.simulator.sensor_generator import generate_sensor_reading


# ============================================================
# Project Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ANOMALY_MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "anomaly_detection"
    / "saved_models"
    / "isolation_forest.joblib"
)

PREPROCESSOR_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "preprocessor.joblib"
)


# ============================================================
# Anomaly Model Features
# ============================================================

ANOMALY_FEATURES = [
    "numerical__Air temperature [K]",
    "numerical__Process temperature [K]",
    "numerical__Rotational speed [rpm]",
    "numerical__Torque [Nm]",
    "numerical__Tool wear [min]"
]


# ============================================================
# Load Model and Preprocessor
# ============================================================

anomaly_model = joblib.load(
    ANOMALY_MODEL_FILE
)

preprocessor = joblib.load(
    PREPROCESSOR_FILE
)


# ============================================================
# Detect Anomaly
# ============================================================

def detect_anomaly(
    sensor_data: dict,
    machine_type: str = "M"
) -> dict:

    raw_data = {
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

    raw_df = pd.DataFrame([raw_data])

    # Use the same preprocessing pipeline as the
    # original project data.
    transformed = preprocessor.transform(
        raw_df
    )

    transformed_df = pd.DataFrame(
        transformed,
        columns=[
            "numerical__Air temperature [K]",
            "numerical__Process temperature [K]",
            "numerical__Rotational speed [rpm]",
            "numerical__Torque [Nm]",
            "numerical__Tool wear [min]",
            "categorical__Type_0",
            "categorical__Type_1",
            "categorical__Type_2"
        ]
    )

    X_anomaly = transformed_df[
        ANOMALY_FEATURES
    ]

    prediction = int(
        anomaly_model.predict(
            X_anomaly
        )[0]
    )

    anomaly_detected = bool(
        prediction == -1
    )

    # Higher value = more anomalous.
    anomaly_score = float(
        -anomaly_model.decision_function(
            X_anomaly
        )[0]
    )

    return {
        "anomaly_detected": anomaly_detected,
        "anomaly_score": round(
            anomaly_score,
            4
        )
    }


# ============================================================
# Validation
# ============================================================

if __name__ == "__main__":

    print("=== ANOMALY MODEL TEST ===")

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

        result = detect_anomaly(
            sensor_data
        )

        print(f"\n--- {scenario_name} ---")

        print(
            f"Anomaly detected: "
            f"{result['anomaly_detected']}"
        )

        print(
            f"Anomaly score: "
            f"{result['anomaly_score']:.4f}"
        )

        if not isinstance(
            result["anomaly_detected"],
            bool
        ):
            all_valid = False

        if not isinstance(
            result["anomaly_score"],
            float
        ):
            all_valid = False

    print("\n=== ANOMALY MODEL VALIDATION ===")

    print(
        f"Model file available: "
        f"{ANOMALY_MODEL_FILE.exists()}"
    )

    print(
        f"Preprocessor available: "
        f"{PREPROCESSOR_FILE.exists()}"
    )

    print(
        f"Required anomaly features: "
        f"{len(ANOMALY_FEATURES)}"
    )

    print(
        f"All anomaly results valid: "
        f"{all_valid}"
    )

    if all_valid:
        print(
            "\nAnomaly detection validation completed successfully!"
        )
    else:
        print(
            "\nAnomaly detection validation failed."
        )