import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "predictive_maintenance"
    / "saved_models"
    / "random_forest_failure_model.joblib"
)


class XAIService:
    def __init__(self):
        package = joblib.load(MODEL_FILE)

        self.model = package["model"]
        self.features = package["features"]
        self.threshold = package["threshold"]

        self.feature_importances = dict(
            zip(
                self.features,
                self.model.feature_importances_
            )
        )

    def get_global_feature_importance(self):
        importance_data = []

        for feature, importance in self.feature_importances.items():
            importance_data.append(
                {
                    "feature": feature,
                    "importance": float(importance),
                    "importance_percent": round(
                        float(importance) * 100, 2
                    )
                }
            )

        importance_data.sort(
            key=lambda x: x["importance"],
            reverse=True
        )

        return importance_data

    def explain_prediction(self, input_data):
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = pd.DataFrame(input_data)

        input_df = input_df[self.features]

        risk_probability = float(
            self.model.predict_proba(input_df)[0, 1]
        )

        if risk_probability >= 0.70:
            risk_level = "Critical"
        elif risk_probability >= self.threshold:
            risk_level = "Warning"
        else:
            risk_level = "Normal"

        return {
            "failure_risk": round(risk_probability, 4),
            "failure_risk_percent": round(
                risk_probability * 100, 2
            ),
            "risk_level": risk_level,
            "feature_importance": self.get_global_feature_importance()
        }


# Reusable service instance
xai_service = XAIService()


if __name__ == "__main__":
    print("=== XAI SERVICE TEST ===")

    print(f"Model loaded: {xai_service.model is not None}")
    print(f"Features loaded: {len(xai_service.features)}")

    print("\n=== GLOBAL FEATURE IMPORTANCE ===")

    for item in xai_service.get_global_feature_importance():
        print(
            f"{item['feature']}: "
            f"{item['importance_percent']:.2f}%"
        )

    print("\nXAI service initialized successfully.")