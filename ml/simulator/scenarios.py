# ============================================================
# Real-Time Machine Simulation Scenarios
# ============================================================

SCENARIOS = {
    "Normal": {
        "description": "Stable machine operating conditions.",
        "sensor_data": {
            "Air temperature [K]": 298.5,
            "Process temperature [K]": 309.5,
            "Rotational speed [rpm]": 1500.0,
            "Torque [Nm]": 40.0,
            "Tool wear [min]": 100.0
        }
    },

    "Warning": {
        "description": "Machine showing elevated operating stress.",
        "sensor_data": {
            "Air temperature [K]": 300.5,
            "Process temperature [K]": 312.5,
            "Rotational speed [rpm]": 1250.0,
            "Torque [Nm]": 50.0,
            "Tool wear [min]": 170.0
        }
    },

    "Critical": {
        "description": "Machine showing severe operating stress.",
        "sensor_data": {
            "Air temperature [K]": 303.5,
            "Process temperature [K]": 316.5,
            "Rotational speed [rpm]": 2400.0,
            "Torque [Nm]": 65.0,
            "Tool wear [min]": 200.0
        }
    }
}


# ============================================================
# Validation
# ============================================================

if __name__ == "__main__":

    print("=== MACHINE SIMULATION SCENARIOS ===")

    required_states = [
        "Normal",
        "Warning",
        "Critical"
    ]

    required_sensors = [
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]

    states_valid = (
        list(SCENARIOS.keys()) == required_states
    )

    sensors_valid = all(
        all(
            sensor in SCENARIOS[state]["sensor_data"]
            for sensor in required_sensors
        )
        for state in required_states
    )

    values_valid = all(
        all(
            isinstance(value, (int, float))
            for value in SCENARIOS[state]["sensor_data"].values()
        )
        for state in required_states
    )

    for state, scenario in SCENARIOS.items():

        print(f"\n--- {state} ---")
        print(scenario["description"])

        for sensor, value in scenario["sensor_data"].items():
            print(f"{sensor}: {value}")

    print("\n=== SCENARIO VALIDATION ===")

    print(f"Required states valid: {states_valid}")
    print(f"Sensor definitions valid: {sensors_valid}")
    print(f"Sensor values valid: {values_valid}")

    all_valid = (
        states_valid
        and sensors_valid
        and values_valid
    )

    print(f"All checks passed: {all_valid}")

    if all_valid:
        print("\nStep 9.2 completed successfully!")
    else:
        print("\nStep 9.2 validation failed.")