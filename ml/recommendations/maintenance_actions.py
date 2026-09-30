from ml.recommendations.recommendation_rules import get_risk_rules


def get_maintenance_action(risk_level):
    """
    Return maintenance actions and priority based on risk level.
    """

    rules = get_risk_rules(risk_level)

    return {
        "priority": rules["priority"],
        "actions": rules["actions"]
    }