import json
import sys
from pathlib import Path
from typing import Any, Dict, List


# Add the project root to Python's import path when this
# file is executed directly.
BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


import joblib
import pandas as pd

from ml.simulator.failure_risk import predict_failure_risk
from ml.simulator.anomaly_detection import detect_anomaly
from ml.recommendations.recommendation_service import (
    generate_recommendations,
)
from ml.explainability.xai_service import xai_service


SIMULATION_OUTPUT_FILE = (
    BASE_DIR
    / "ml"
    / "simulator"
    / "saved_outputs"
    / "latest_simulation.json"
)

TEMPERATURE_HISTORY_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "temperature_test.csv"
)

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


class IndustrialCopilotService:
    """
    Grounded AI Industrial Copilot service.

    Provides structured access to the project's existing
    machine-analysis systems and verified project data.
    """

    def __init__(self):
        self.name = "AI Industrial Copilot"
        self.version = "1.0"

    def get_machine_status(
        self,
        sensor_data: Dict[str, float],
        machine_type: str = "M",
    ) -> Dict[str, Any]:
        risk_result = predict_failure_risk(
            sensor_data=sensor_data,
            machine_type=machine_type,
        )

        anomaly_result = detect_anomaly(
            sensor_data=sensor_data,
            machine_type=machine_type,
        )

        return {
            "machine_status": risk_result["risk_level"],
            "failure_risk": risk_result["failure_risk"],
            "predicted_failure": risk_result["predicted_failure"],
            "anomaly_detected": anomaly_result["anomaly_detected"],
            "anomaly_score": anomaly_result["anomaly_score"],
        }

    def get_failure_risk(
        self,
        sensor_data: Dict[str, float],
        machine_type: str = "M",
    ) -> Dict[str, Any]:
        result = predict_failure_risk(
            sensor_data=sensor_data,
            machine_type=machine_type,
        )

        return {
            "failure_risk": result["failure_risk"],
            "predicted_failure": result["predicted_failure"],
            "risk_level": result["risk_level"],
            "threshold": result.get(
                "threshold",
                0.40,
            ),
        }

    def get_anomaly_status(
        self,
        sensor_data: Dict[str, float],
        machine_type: str = "M",
    ) -> Dict[str, Any]:
        result = detect_anomaly(
            sensor_data=sensor_data,
            machine_type=machine_type,
        )

        return {
            "anomaly_detected": result["anomaly_detected"],
            "anomaly_score": result["anomaly_score"],
        }

    def get_recent_anomalies(
        self,
        limit: int = 10,
    ) -> Dict[str, Any]:
        if not SIMULATION_OUTPUT_FILE.exists():
            return {
                "source": "simulator",
                "anomalies": [],
                "count": 0,
                "message": (
                    "No saved simulation output is available."
                ),
            }

        with open(
            SIMULATION_OUTPUT_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            simulation_data = json.load(file)

        anomaly_detected = bool(
            simulation_data.get(
                "anomaly_detected",
                False,
            )
        )

        if not anomaly_detected:
            return {
                "source": "simulator",
                "anomalies": [],
                "count": 0,
                "message": (
                    "No anomaly detected in the latest simulation."
                ),
            }

        anomaly_record = {
            "machine_id": simulation_data.get(
                "machine_id",
                "SIM-CNC-01",
            ),
            "scenario": simulation_data.get(
                "scenario",
                "Unknown",
            ),
            "anomaly_detected": anomaly_detected,
            "anomaly_score": simulation_data.get(
                "anomaly_score",
                0.0,
            ),
            "failure_risk": simulation_data.get(
                "failure_risk",
                0.0,
            ),
            "risk_level": simulation_data.get(
                "risk_level",
                "Unknown",
            ),
        }

        anomalies = [anomaly_record][
            :max(1, limit)
        ]

        return {
            "source": "simulator",
            "anomalies": anomalies,
            "count": len(anomalies),
            "message": (
                "Latest verified simulator anomaly retrieved."
            ),
        }

    def get_machine_history(
        self,
        limit: int = 12,
    ) -> Dict[str, Any]:
        if not TEMPERATURE_HISTORY_FILE.exists():
            return {
                "source": "forecasting_test_data",
                "sensor": "temperature",
                "history": [],
                "count": 0,
                "message": (
                    "Temperature history file is not available."
                ),
            }

        dataframe = pd.read_csv(
            TEMPERATURE_HISTORY_FILE
        )

        if "temperature" not in dataframe.columns:
            return {
                "source": "forecasting_test_data",
                "sensor": "temperature",
                "history": [],
                "count": 0,
                "message": (
                    "Temperature column was not found."
                ),
            }

        values = (
            dataframe["temperature"]
            .dropna()
            .astype(float)
            .tolist()
        )

        recent_values = values[
            -max(1, limit):
        ]

        history = [
            {
                "reading_number": index + 1,
                "temperature": round(
                    value,
                    4,
                ),
            }
            for index, value in enumerate(
                recent_values
            )
        ]

        return {
            "source": "forecasting_test_data",
            "sensor": "temperature",
            "history": history,
            "count": len(history),
            "message": (
                "Recent verified temperature history retrieved."
            ),
        }

    def get_forecast(
        self,
        temperature_history: List[float],
    ) -> Dict[str, Any]:
        if len(temperature_history) < 12:
            return {
                "sensor": "temperature",
                "forecast": None,
                "history_points": len(
                    temperature_history
                ),
                "message": (
                    "At least 12 temperature readings "
                    "are required."
                ),
            }

        values = temperature_history[-12:]

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
            "history_points": len(
                temperature_history
            ),
            "model": "Random Forest",
            "forecast_horizon": "Next Reading",
        }

    def get_explanation(
        self,
        sensor_data: Dict[str, float],
        machine_type: str = "M",
    ) -> Dict[str, Any]:
        raw_data = {
            **sensor_data,
            "Type": machine_type,
        }

        raw_dataframe = pd.DataFrame(
            [raw_data]
        )

        transformed_data = (
            preprocessor.transform(
                raw_dataframe
            )
        )

        transformed_dataframe = pd.DataFrame(
            transformed_data,
            columns=xai_service.features,
        )

        explanation = (
            xai_service.explain_prediction(
                transformed_dataframe
            )
        )

        return {
            "method": (
                "Random Forest built-in "
                "feature importance"
            ),
            "machine_type": machine_type,
            "explanation": explanation,
        }

    def get_recommendations(
        self,
        sensor_data: Dict[str, float],
        machine_type: str = "M",
    ) -> Dict[str, Any]:
        risk_result = predict_failure_risk(
            sensor_data=sensor_data,
            machine_type=machine_type,
        )

        anomaly_result = detect_anomaly(
            sensor_data=sensor_data,
            machine_type=machine_type,
        )

        return generate_recommendations(
            risk_level=risk_result["risk_level"],
            sensor_data=sensor_data,
            anomaly_detected=anomaly_result[
                "anomaly_detected"
            ],
            anomaly_score=anomaly_result[
                "anomaly_score"
            ],
        )

    def process_query(
        self,
        query: str,
        sensor_data: Dict[str, float],
        machine_type: str = "M",
    ) -> Dict[str, Any]:
        """
        Route a natural-language Copilot query to the
        appropriate verified project tool.
        """

        normalized_query = query.strip().lower()

        if not normalized_query:
            return {
                "success": False,
                "tool": None,
                "message": (
                    "Please enter a machine-related question."
                ),
            }

        # Recommendation / maintenance questions
        if any(
            keyword in normalized_query
            for keyword in [
                "recommendation",
                "recommendations",
                "maintenance",
                "maintain",
                "action",
                "actions",
                "what should",
            ]
        ):
            return {
                "success": True,
                "tool": "get_recommendations",
                "result": self.get_recommendations(
                    sensor_data=sensor_data,
                    machine_type=machine_type,
                ),
            }

        # Explanation / XAI questions
        if any(
            keyword in normalized_query
            for keyword in [
                "explain",
                "explanation",
                "why",
                "important feature",
                "feature importance",
                "xai",
            ]
        ):
            return {
                "success": True,
                "tool": "get_explanation",
                "result": self.get_explanation(
                    sensor_data=sensor_data,
                    machine_type=machine_type,
                ),
            }

        # Forecast questions
        if any(
            keyword in normalized_query
            for keyword in [
                "forecast",
                "forecasting",
                "predict temperature",
                "future temperature",
                "next temperature",
            ]
        ):
            history_result = self.get_machine_history(
                limit=12
            )

            history_values = [
                item["temperature"]
                for item in history_result[
                    "history"
                ]
            ]

            return {
                "success": True,
                "tool": "get_forecast",
                "result": self.get_forecast(
                    temperature_history=history_values
                ),
            }

        # Anomaly questions
        if any(
            keyword in normalized_query
            for keyword in [
                "anomaly",
                "anomalies",
                "abnormal",
                "abnormality",
            ]
        ):
            return {
                "success": True,
                "tool": "get_recent_anomalies",
                "result": self.get_recent_anomalies(),
            }

        # Failure-risk questions
        if any(
            keyword in normalized_query
            for keyword in [
                "failure risk",
                "risk",
                "fail",
                "failure",
                "breakdown",
            ]
        ):
            return {
                "success": True,
                "tool": "get_failure_risk",
                "result": self.get_failure_risk(
                    sensor_data=sensor_data,
                    machine_type=machine_type,
                ),
            }

        # History questions
        if any(
            keyword in normalized_query
            for keyword in [
                "history",
                "historical",
                "recent readings",
                "recent temperature",
                "readings",
            ]
        ):
            return {
                "success": True,
                "tool": "get_machine_history",
                "result": self.get_machine_history(),
            }

        # General machine-status questions
        if any(
            keyword in normalized_query
            for keyword in [
                "status",
                "condition",
                "health",
                "machine",
                "current",
            ]
        ):
            return {
                "success": True,
                "tool": "get_machine_status",
                "result": self.get_machine_status(
                    sensor_data=sensor_data,
                    machine_type=machine_type,
                ),
            }

        return {
            "success": False,
            "tool": None,
            "message": (
                "I can currently help with machine status, "
                "failure risk, anomalies, history, forecasting, "
                "explanations, and maintenance recommendations."
            ),
        }


copilot_service = IndustrialCopilotService()


if __name__ == "__main__":
    print(
        "=== AI INDUSTRIAL COPILOT QUERY PROCESSING TEST ==="
    )

    sample_sensor_data = {
        "Air temperature [K]": 303.5,
        "Process temperature [K]": 316.5,
        "Rotational speed [rpm]": 2400.0,
        "Torque [Nm]": 65.0,
        "Tool wear [min]": 200.0,
    }

    test_queries = [
        "What is the current machine status?",
        "What is the failure risk?",
        "Are there any recent anomalies?",
        "Show me the recent machine history.",
        "What is the temperature forecast?",
        "Explain the prediction.",
        "What maintenance actions are recommended?",
    ]

    for query in test_queries:
        result = copilot_service.process_query(
            query=query,
            sensor_data=sample_sensor_data,
            machine_type="M",
        )

        print("\nQuery:")
        print(query)

        print("Selected Tool:")
        print(result["tool"])

        print("Success:")
        print(result["success"])

    print(
        "\nCopilot query processing initialized successfully."
    )