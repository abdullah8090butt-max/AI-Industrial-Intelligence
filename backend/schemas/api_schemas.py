from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List


class HealthResponse(BaseModel):
    status: str
    project: str
    environment: str


class MachineSensorData(BaseModel):
    air_temperature: float = Field(
        ...,
        ge=290.0,
        le=310.0,
        description="Air temperature in Kelvin."
    )

    process_temperature: float = Field(
        ...,
        ge=300.0,
        le=325.0,
        description="Process temperature in Kelvin."
    )

    rotational_speed: float = Field(
        ...,
        ge=500.0,
        le=3000.0,
        description="Rotational speed in RPM."
    )

    torque: float = Field(
        ...,
        ge=0.0,
        le=80.0,
        description="Machine torque in Nm."
    )

    tool_wear: float = Field(
        ...,
        ge=0.0,
        le=250.0,
        description="Tool wear in minutes."
    )

    machine_type: Optional[str] = "M"


class FailureRiskResponse(BaseModel):
    failure_risk: float
    predicted_failure: bool
    risk_level: str


class AnomalyResponse(BaseModel):
    anomaly_detected: bool
    anomaly_score: float


class RecommendationResponse(BaseModel):
    risk_level: str
    maintenance: Dict[str, Any]
    sensor: Any
    anomaly: Any


class ForecastRequest(BaseModel):
    temperature_history: List[float] = Field(
        ...,
        min_length=12,
        description="Recent temperature readings in chronological order."
    )


class ForecastResponse(BaseModel):
    sensor: str
    forecast: float
    history_points: int


class CopilotQueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Natural-language industrial machine question."
    )

    sensor_data: MachineSensorData