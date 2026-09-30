import sys
import time
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from ml.simulator.live_recommendations import generate_live_recommendation


# Lightweight simulation interval.
# One second keeps the simulator responsive without unnecessary waiting.
UPDATE_INTERVAL = 1


def run_simulation(scenario_name, cycles=5):
    """
    Run a lightweight real-time machine simulation.

    Each cycle:
        1. Generates new sensor readings.
        2. Calculates failure risk.
        3. Detects anomalies.
        4. Generates maintenance recommendations.
    """

    print("=" * 60)
    print("AI INDUSTRIAL INTELLIGENCE")
    print("REAL-TIME MACHINE SIMULATION")
    print("=" * 60)

    print(f"Scenario: {scenario_name}")
    print(f"Cycles: {cycles}")
    print(f"Update interval: {UPDATE_INTERVAL} second")

    for cycle in range(1, cycles + 1):

        result = generate_live_recommendation(
            scenario_name,
            seed=cycle
        )

        print("\n" + "-" * 60)
        print(f"Cycle {cycle}/{cycles}")
        print("-" * 60)

        print(f"Failure Risk       : {result['failure_risk']:.4f}")
        print(f"Risk Level         : {result['risk_level']}")
        print(f"Predicted Failure  : {result['predicted_failure']}")
        print(f"Anomaly Detected   : {result['anomaly_detected']}")
        print(f"Anomaly Score      : {result['anomaly_score']:.4f}")

        print("\nSensor Readings:")

        for sensor, value in result["sensor_data"].items():
            print(f"  {sensor}: {value}")

        print("\nMaintenance Priority:")

        priority = result["recommendations"]["maintenance"]["priority"]
        print(f"  {priority}")

        if cycle < cycles:
            time.sleep(UPDATE_INTERVAL)

    print("\n" + "=" * 60)
    print("SIMULATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_simulation(
        scenario_name="Critical",
        cycles=5
    )