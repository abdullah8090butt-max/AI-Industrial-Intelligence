from pydantic import BaseModel
from typing import Dict, Any, Optional


class HealthResponse(BaseModel):
    status: str
    project: str
    environment: str


class MachineSensorData(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
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
    sensor: Dict[str, Any]
    anomaly: Dict[str, Any]