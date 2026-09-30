import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from ml.simulator.sensor_generator import generate_sensor_reading
from ml.simulator.failure_risk import predict_failure_risk
from ml.simulator.anomaly_detection import detect_anomaly
from ml.recommendations.recommendation_service import generate_recommendations


def generate_live_recommendation(scenario_name, seed=None):
    """
    Generate one complete simulated machine-health result.

    Pipeline:
    Sensor reading
        -> Failure risk
        -> Anomaly detection
        -> Maintenance recommendation
    """

    sensor_data = generate_sensor_reading(
        scenario_name,
        seed=seed
    )

    risk_result = predict_failure_risk(sensor_data)

    anomaly_result = detect_anomaly(sensor_data)

    recommendation_result = generate_recommendations(
        risk_level=risk_result["risk_level"],
        sensor_data=sensor_data,
        anomaly_detected=anomaly_result["anomaly_detected"],
        anomaly_score=anomaly_result["anomaly_score"]
    )

    return {
        "scenario": scenario_name,
        "sensor_data": sensor_data,
        "failure_risk": risk_result["failure_risk"],
        "predicted_failure": risk_result["predicted_failure"],
        "risk_level": risk_result["risk_level"],
        "anomaly_detected": anomaly_result["anomaly_detected"],
        "anomaly_score": anomaly_result["anomaly_score"],
        "recommendations": recommendation_result
    }


def validate_live_recommendations():
    """Validate live recommendation generation."""

    scenarios = ["Normal", "Warning", "Critical"]

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

    all_valid = True

    for scenario in scenarios:
        result = generate_live_recommendation(
            scenario,
            seed=42
        )

        print(f"\n--- {scenario} ---")
        print(f"Failure risk: {result['failure_risk']:.4f}")
        print(f"Predicted failure: {result['predicted_failure']}")
        print(f"Risk level: {result['risk_level']}")
        print(f"Anomaly detected: {result['anomaly_detected']}")
        print(f"Anomaly score: {result['anomaly_score']:.4f}")

        print("Recommendations:")
        print(result["recommendations"])

        if not required_keys.issubset(result.keys()):
            all_valid = False

        if not isinstance(result["sensor_data"], dict):
            all_valid = False

        if not isinstance(result["failure_risk"], float):
            all_valid = False

        if not isinstance(result["predicted_failure"], bool):
            all_valid = False

        if result["risk_level"] not in {"Normal", "Warning", "Critical"}:
            all_valid = False

        if not isinstance(result["anomaly_detected"], bool):
            all_valid = False

        if not isinstance(result["anomaly_score"], float):
            all_valid = False

    print("\n=== LIVE RECOMMENDATION VALIDATION ===")
    print(f"All live results valid: {all_valid}")

    if not all_valid:
        raise AssertionError("Live recommendation validation failed.")

    print("\nStep 9.6 completed successfully!")


if __name__ == "__main__":
    validate_live_recommendations()