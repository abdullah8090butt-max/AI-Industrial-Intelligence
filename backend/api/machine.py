from fastapi import APIRouter

from backend.schemas.api_schemas import (
    MachineSensorData,
    ForecastRequest,
    CopilotQueryRequest,
)

from backend.services.copilot_service import (
    copilot_service,
)

from ml.simulator.failure_risk import predict_failure_risk
from ml.simulator.anomaly_detection import detect_anomaly
from ml.recommendations.recommendation_service import (
    generate_recommendations,
)
from ml.explainability.xai_service import xai_service

import joblib
import pandas as pd
from pathlib import Path


router = APIRouter(
    prefix="/machine",
    tags=["Machine"],
)


BASE_DIR = Path(__file__).resolve().parents[2]


FORECAST_MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "forecasting"
    / "saved_models"
    / "temperature_forecasting_model.joblib"
)


PREPROCESSOR_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "preprocessor.joblib"
)


forecast_package = joblib.load(
    FORECAST_MODEL_FILE
)

forecast_model = forecast_package["model"]

preprocessor = joblib.load(
    PREPROCESSOR_FILE
)


def build_sensor_data(
    sensor_data: MachineSensorData,
) -> dict:
    return {
        "Air temperature [K]":
            sensor_data.air_temperature,

        "Process temperature [K]":
            sensor_data.process_temperature,

        "Rotational speed [rpm]":
            sensor_data.rotational_speed,

        "Torque [Nm]":
            sensor_data.torque,

        "Tool wear [min]":
            sensor_data.tool_wear,
    }


@router.post("/status")
def get_machine_status(
    sensor_data: MachineSensorData,
):
    data = build_sensor_data(
        sensor_data
    )

    risk_result = predict_failure_risk(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )

    anomaly_result = detect_anomaly(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )

    return {
        "machine_status":
            risk_result["risk_level"],

        "failure_risk":
            risk_result["failure_risk"],

        "predicted_failure":
            risk_result["predicted_failure"],

        "anomaly_detected":
            anomaly_result["anomaly_detected"],

        "anomaly_score":
            anomaly_result["anomaly_score"],

        "sensor_data":
            data,
    }


@router.post("/failure-risk")
def get_failure_risk(
    sensor_data: MachineSensorData,
):
    data = build_sensor_data(
        sensor_data
    )

    result = predict_failure_risk(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )

    return result


@router.post("/anomaly")
def get_anomaly_status(
    sensor_data: MachineSensorData,
):
    data = build_sensor_data(
        sensor_data
    )

    result = detect_anomaly(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )

    return result


@router.post("/recommendations")
def get_machine_recommendations(
    sensor_data: MachineSensorData,
):
    data = build_sensor_data(
        sensor_data
    )

    risk_result = predict_failure_risk(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )

    anomaly_result = detect_anomaly(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )

    recommendations = generate_recommendations(
        risk_level=risk_result["risk_level"],
        sensor_data=data,
        anomaly_detected=
            anomaly_result["anomaly_detected"],
        anomaly_score=
            anomaly_result["anomaly_score"],
    )

    return recommendations


@router.post("/forecast")
def get_temperature_forecast(
    request: ForecastRequest,
):
    history = request.temperature_history

    if len(history) < 12:
        return {
            "error":
                "At least 12 temperature readings are required."
        }

    values = history[-12:]

    forecast_input = {
        "lag_1": values[-1],
        "lag_2": values[-2],
        "lag_3": values[-3],
        "lag_6": values[-6],
        "lag_12": values[-12],
        "hour": 12,
        "day_of_week": 0,
    }

    X_forecast = pd.DataFrame(
        [forecast_input]
    )

    prediction = float(
        forecast_model.predict(
            X_forecast
        )[0]
    )

    return {
        "sensor": "temperature",
        "forecast": round(
            prediction,
            4,
        ),
        "history_points":
            len(history),
    }


@router.post("/explanation")
def get_machine_explanation(
    sensor_data: MachineSensorData,
):
    data = build_sensor_data(
        sensor_data
    )

    machine_type = (
        sensor_data.machine_type
    )

    raw_data = {
        **data,
        "Type": machine_type,
    }

    raw_df = pd.DataFrame(
        [raw_data]
    )

    transformed_data = (
        preprocessor.transform(
            raw_df
        )
    )

    transformed_df = pd.DataFrame(
        transformed_data,
        columns=xai_service.features,
    )

    explanation = (
        xai_service.explain_prediction(
            transformed_df
        )
    )

    return {
        "sensor_data": data,
        "machine_type":
            machine_type,
        "explanation":
            explanation,
    }


# ============================================================
# AI INDUSTRIAL COPILOT TOOLS
# ============================================================

@router.post("/copilot/status")
def get_copilot_machine_status(
    sensor_data: MachineSensorData,
):
    """
    Copilot tool:
    Returns the current machine health status
    using the project's real AI models.
    """

    data = build_sensor_data(
        sensor_data
    )

    return copilot_service.get_machine_status(
        sensor_data=data,
        machine_type=sensor_data.machine_type,
    )


@router.post("/copilot/query")
def process_copilot_query(
    request: CopilotQueryRequest,
):
    """
    Main AI Industrial Copilot endpoint.

    Routes the user's natural-language question to
    the appropriate verified project tool.
    """

    sensor_data = build_sensor_data(
        request.sensor_data
    )

    result = copilot_service.process_query(
        query=request.query,
        sensor_data=sensor_data,
        machine_type=request.sensor_data.machine_type,
    )

    return {
        "query": request.query,
        "copilot": result,
    }