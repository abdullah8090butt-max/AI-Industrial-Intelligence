from ml.recommendations.maintenance_actions import get_maintenance_action
from ml.recommendations.sensor_recommendations import get_sensor_recommendations
from ml.recommendations.anomaly_recommendations import get_anomaly_recommendations


def generate_recommendations(
    risk_level,
    sensor_data,
    anomaly_detected,
    anomaly_score
):
    """
    Combine maintenance, sensor, and anomaly recommendations
    into one complete recommendation result.
    """

    maintenance_result = get_maintenance_action(risk_level)

    sensor_result = get_sensor_recommendations(sensor_data)

    anomaly_result = get_anomaly_recommendations(
        anomaly_detected=anomaly_detected,
        anomaly_score=anomaly_score
    )

    return {
        "risk_level": risk_level,
        "maintenance": maintenance_result,
        "sensor": sensor_result,
        "anomaly": anomaly_result
    }