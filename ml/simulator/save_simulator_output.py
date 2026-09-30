import sys
import json
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from ml.simulator.live_recommendations import generate_live_recommendation


OUTPUT_DIR = PROJECT_ROOT / "ml" / "simulator" / "saved_outputs"
OUTPUT_FILE = OUTPUT_DIR / "latest_simulation.json"


def save_simulation_output():
    """
    Generate one complete simulator result,
    save it as JSON, and validate the saved file.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate a real simulator result
    result = generate_live_recommendation(
        scenario_name="Critical",
        seed=42
    )

    # Save result
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=4
        )

    print("=== SIMULATOR OUTPUT SAVE ===")
    print(f"Output file created: {OUTPUT_FILE.exists()}")

    print("\n=== GENERATED RESULT ===")
    print(f"Scenario: {result['scenario']}")
    print(f"Failure risk: {result['failure_risk']:.4f}")
    print(f"Risk level: {result['risk_level']}")
    print(f"Predicted failure: {result['predicted_failure']}")
    print(f"Anomaly detected: {result['anomaly_detected']}")
    print(f"Anomaly score: {result['anomaly_score']:.4f}")

    # Reload saved JSON
    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        loaded_result = json.load(file)

    reload_successful = loaded_result == result

    print("\n=== SAVED OUTPUT VALIDATION ===")
    print(f"JSON reload successful: {reload_successful}")

    required_keys = {
        "scenario",
        "sensor_data",
        "failure_risk",
        "predicted_failure",
        "risk_level",
        "anomaly_detected",
        "anomaly_score",
        "recommendations"
    }

    keys_valid = required_keys.issubset(loaded_result.keys())

    print(f"Required fields present: {keys_valid}")

    all_valid = (
        OUTPUT_FILE.exists()
        and reload_successful
        and keys_valid
    )

    print(f"All validation checks passed: {all_valid}")

    if not all_valid:
        raise AssertionError(
            "Simulator output validation failed."
        )

    print("\nFINAL RESULT")
    print("Simulator output saved and validated successfully!")
    print("\nPhase 9 completed successfully!")


if __name__ == "__main__":
    save_simulation_output()