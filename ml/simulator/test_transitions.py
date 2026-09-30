import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from ml.simulator.live_recommendations import generate_live_recommendation


SCENARIO_SEQUENCE = [
    "Normal",
    "Warning",
    "Critical",
    "Normal"
]


def test_scenario_transitions():
    print("=" * 60)
    print("SCENARIO TRANSITION TEST")
    print("=" * 60)

    results = []
    all_valid = True

    for index, scenario in enumerate(SCENARIO_SEQUENCE, start=1):

        result = generate_live_recommendation(
            scenario_name=scenario,
            seed=index
        )

        results.append(result)

        print(f"\nTransition {index}: {scenario}")
        print("-" * 60)
        print(f"Failure Risk      : {result['failure_risk']:.4f}")
        print(f"Risk Level        : {result['risk_level']}")
        print(f"Predicted Failure : {result['predicted_failure']}")
        print(f"Anomaly Detected  : {result['anomaly_detected']}")
        print(f"Anomaly Score     : {result['anomaly_score']:.4f}")

        # Validate result structure
        if result["scenario"] != scenario:
            all_valid = False

        if result["risk_level"] not in {"Normal", "Warning", "Critical"}:
            all_valid = False

        if not isinstance(result["predicted_failure"], bool):
            all_valid = False

        if not isinstance(result["anomaly_detected"], bool):
            all_valid = False

        if not isinstance(result["failure_risk"], float):
            all_valid = False

        if not isinstance(result["anomaly_score"], float):
            all_valid = False

    print("\n" + "=" * 60)
    print("TRANSITION VALIDATION")
    print("=" * 60)

    print(f"Scenarios tested: {len(SCENARIO_SEQUENCE)}")
    print(f"Sequence valid: {results[0]['scenario'] == 'Normal'}")
    print(f"All transition results valid: {all_valid}")

    if not all_valid:
        raise AssertionError("Scenario transition validation failed.")

    print("\nStep 9.8 completed successfully!")


if __name__ == "__main__":
    test_scenario_transitions()