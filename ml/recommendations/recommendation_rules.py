RECOMMENDATION_RULES = {
    "Critical": {
        "priority": "High",
        "actions": [
            "Schedule immediate machine inspection.",
            "Check torque and rotational speed conditions.",
            "Inspect tool wear and machine operating condition.",
            "Review recent anomaly and failure-risk signals before continued operation."
        ]
    },

    "Warning": {
        "priority": "Medium",
        "actions": [
            "Schedule preventive maintenance inspection.",
            "Monitor torque and rotational speed closely.",
            "Check tool wear and temperature conditions.",
            "Continue monitoring the machine for increasing risk."
        ]
    },

    "Normal": {
        "priority": "Low",
        "actions": [
            "Continue normal machine operation.",
            "Maintain routine preventive maintenance schedule.",
            "Continue monitoring sensor conditions."
        ]
    }
}


FEATURE_RECOMMENDATIONS = {
    "torque": {
        "keywords": ["torque"],
        "action": "Inspect torque conditions and check for abnormal load."
    },

    "rotational_speed": {
        "keywords": ["rotational speed"],
        "action": "Check rotational speed for unusual operating conditions."
    },

    "tool_wear": {
        "keywords": ["tool wear"],
        "action": "Inspect tool wear and consider maintenance or replacement if excessive."
    },

    "temperature": {
        "keywords": [
            "air temperature",
            "process temperature"
        ],
        "action": "Check machine temperature conditions and cooling/thermal behavior."
    }
}


def get_risk_rules(risk_level):
    return RECOMMENDATION_RULES.get(
        risk_level,
        RECOMMENDATION_RULES["Normal"]
    )


if __name__ == "__main__":
    print("=== RECOMMENDATION RULES TEST ===")

    for risk_level in ["Normal", "Warning", "Critical"]:
        rules = get_risk_rules(risk_level)

        print(f"\n{risk_level}")
        print(f"Priority: {rules['priority']}")

        for action in rules["actions"]:
            print(f"- {action}")

    print("\nRecommendation rules loaded successfully.")