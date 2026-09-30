from pathlib import Path


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
# Machine States
# ============================================================

MACHINE_STATES = [
    "Normal",
    "Warning",
    "Critical"
]


# ============================================================
# Default Machine Sensor Inputs
# ============================================================

DEFAULT_SENSOR_DATA = {
    "Air temperature [K]": 298.5,
    "Process temperature [K]": 309.5,
    "Rotational speed [rpm]": 1500.0,
    "Torque [Nm]": 40.0,
    "Tool wear [min]": 100.0
}


# ============================================================
# Simulator Settings
# ============================================================

SIMULATOR_CONFIG = {
    "default_machine_id": "SIM-CNC-01",
    "update_interval_seconds": 1,
    "supported_states": MACHINE_STATES,
    "sensor_units": {
        "Air temperature [K]": "K",
        "Process temperature [K]": "K",
        "Rotational speed [rpm]": "rpm",
        "Torque [Nm]": "Nm",
        "Tool wear [min]": "min"
    }
}


# ============================================================
# Validation
# ============================================================

if __name__ == "__main__":

    print("=== SIMULATOR CONFIGURATION ===")

    print(
        f"Default machine: "
        f"{SIMULATOR_CONFIG['default_machine_id']}"
    )

    print(
        f"Supported states: "
        f"{', '.join(MACHINE_STATES)}"
    )

    print("\n=== DEFAULT SENSOR INPUTS ===")

    for sensor, value in DEFAULT_SENSOR_DATA.items():
        unit = SIMULATOR_CONFIG["sensor_units"][sensor]
        print(f"{sensor}: {value} {unit}")

    print("\n=== CONFIGURATION VALIDATION ===")

    paths_valid = (
        FAILURE_MODEL_FILE.exists()
        and ANOMALY_MODEL_FILE.exists()
        and PREPROCESSOR_FILE.exists()
    )

    states_valid = (
        len(MACHINE_STATES) == 3
        and all(
            state in ["Normal", "Warning", "Critical"]
            for state in MACHINE_STATES
        )
    )

    sensors_valid = (
        len(DEFAULT_SENSOR_DATA) == 5
        and all(
            sensor in SIMULATOR_CONFIG["sensor_units"]
            for sensor in DEFAULT_SENSOR_DATA
        )
    )

    print(
        f"Required model files available: "
        f"{paths_valid}"
    )

    print(
        f"Machine states valid: "
        f"{states_valid}"
    )

    print(
        f"Sensor inputs valid: "
        f"{sensors_valid}"
    )

    all_valid = (
        paths_valid
        and states_valid
        and sensors_valid
    )

    print(
        f"All checks passed: "
        f"{all_valid}"
    )

    if all_valid:
        print(
            "\nStep 9.1 completed successfully!"
        )
    else:
        print(
            "\nStep 9.1 validation failed."
        )