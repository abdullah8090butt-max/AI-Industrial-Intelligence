import random

from ml.simulator.scenarios import SCENARIOS


# ============================================================
# Sensor Variation Settings
# ============================================================

SENSOR_VARIATION = {
    "Air temperature [K]": 0.5,
    "Process temperature [K]": 0.5,
    "Rotational speed [rpm]": 50.0,
    "Torque [Nm]": 2.0,
    "Tool wear [min]": 1.0
}


# ============================================================
# Sensor Bounds
# ============================================================

SENSOR_BOUNDS = {
    "Air temperature [K]": (290.0, 310.0),
    "Process temperature [K]": (300.0, 325.0),
    "Rotational speed [rpm]": (500.0, 3000.0),
    "Torque [Nm]": (0.0, 80.0),
    "Tool wear [min]": (0.0, 250.0)
}


# ============================================================
# Generate One Sensor Reading
# ============================================================

def generate_sensor_reading(
    scenario_name: str,
    seed: int | None = None
) -> dict:

    if scenario_name not in SCENARIOS:
        raise ValueError(
            f"Unknown scenario: {scenario_name}"
        )

    if seed is not None:
        random.seed(seed)

    base_data = SCENARIOS[scenario_name]["sensor_data"]

    reading = {}

    for sensor, base_value in base_data.items():

        variation = SENSOR_VARIATION[sensor]

        value = (
            base_value
            + random.uniform(
                -variation,
                variation
            )
        )

        minimum, maximum = SENSOR_BOUNDS[sensor]

        value = max(
            minimum,
            min(maximum, value)
        )

        reading[sensor] = round(
            float(value),
            3
        )

    return reading


# ============================================================
# Validation
# ============================================================

if __name__ == "__main__":

    print("=== SENSOR READING GENERATOR ===")

    required_sensors = list(
        SENSOR_VARIATION.keys()
    )

    all_valid = True

    for scenario_name in [
        "Normal",
        "Warning",
        "Critical"
    ]:

        reading = generate_sensor_reading(
            scenario_name,
            seed=42
        )

        print(f"\n--- {scenario_name} ---")

        for sensor, value in reading.items():

            minimum, maximum = SENSOR_BOUNDS[sensor]

            print(
                f"{sensor}: {value}"
            )

            if not (
                sensor in required_sensors
                and minimum <= value <= maximum
            ):
                all_valid = False

        if len(reading) != len(required_sensors):
            all_valid = False

    print("\n=== GENERATOR VALIDATION ===")

    print(
        f"Sensor count valid: "
        f"{all_valid}"
    )

    print(
        f"All generated readings valid: "
        f"{all_valid}"
    )

    if all_valid:
        print(
            "\nStep 9.3 completed successfully!"
        )
    else:
        print(
            "\nStep 9.3 validation failed."
        )