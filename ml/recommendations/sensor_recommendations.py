def get_sensor_recommendations(sensor_data):
    recommendations = []

    torque = sensor_data.get("Torque [Nm]")
    rotational_speed = sensor_data.get("Rotational speed [rpm]")
    tool_wear = sensor_data.get("Tool wear [min]")
    air_temperature = sensor_data.get("Air temperature [K]")
    process_temperature = sensor_data.get("Process temperature [K]")

    # Torque
    if torque is not None:
        if torque >= 50:
            recommendations.append(
                "Inspect torque conditions for unusually high machine load."
            )

    # Rotational speed
    if rotational_speed is not None:
        if rotational_speed <= 1200:
            recommendations.append(
                "Check rotational speed for unusually low operating speed."
            )
        elif rotational_speed >= 2200:
            recommendations.append(
                "Check rotational speed for unusually high operating speed."
            )

    # Tool wear
    if tool_wear is not None:
        if tool_wear >= 180:
            recommendations.append(
                "Inspect tool wear and consider tool maintenance or replacement."
            )

    # Temperature difference
    if (
        air_temperature is not None
        and process_temperature is not None
    ):
        temperature_difference = (
            process_temperature - air_temperature
        )

        if temperature_difference >= 12:
            recommendations.append(
                "Check thermal conditions because the process-to-air "
                "temperature difference is elevated."
            )

    if not recommendations:
        recommendations.append(
            "No specific sensor-based maintenance condition detected."
        )

    return recommendations


if __name__ == "__main__":
    print("=== SENSOR RECOMMENDATION TEST ===")

    test_sensor_data = {
        "Torque [Nm]": 55,
        "Rotational speed [rpm]": 1100,
        "Tool wear [min]": 190,
        "Air temperature [K]": 300,
        "Process temperature [K]": 313
    }

    recommendations = get_sensor_recommendations(
        test_sensor_data
    )

    for recommendation in recommendations:
        print(f"- {recommendation}")

    print("\nSensor recommendation logic successful.")