def get_anomaly_recommendations(anomaly_detected, anomaly_score=None):
    recommendations = []

    if anomaly_detected:
        recommendations.append(
            "Investigate the detected machine anomaly."
        )

        if anomaly_score is not None:
            recommendations.append(
                f"Review the anomaly score ({anomaly_score:.3f}) "
                "alongside current machine conditions."
            )

        recommendations.append(
            "Check recent sensor readings and machine operating conditions."
        )
    else:
        recommendations.append(
            "No anomaly detected by the anomaly detection model."
        )

    return recommendations


if __name__ == "__main__":
    print("=== ANOMALY RECOMMENDATION TEST ===")

    recommendations = get_anomaly_recommendations(
        anomaly_detected=True,
        anomaly_score=0.82
    )

    for recommendation in recommendations:
        print(f"- {recommendation}")

    print("\nAnomaly recommendation logic successful.")