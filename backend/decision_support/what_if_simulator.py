def simulate_action(
    overall_score,
    action
):
    """
    Simulate how a hypothetical farm-management action
    could change the estimated farm risk score.

    This is a prototype simulation based on decision rules.
    It does not predict guaranteed real-world outcomes.
    """

    action = action.lower().strip()

    adjustments = {
        "increase irrigation": -10,
        "reduce irrigation": 5,
        "apply fertilizer": -7,
        "improve drainage": -12,
        "use disease control": -10,
        "monitor crop closely": -5,
        "take no action": 0
    }

    adjustment = adjustments.get(action)

    if adjustment is None:
        return {
            "status": "error",
            "message": (
                "Unknown action. Choose from: "
                "increase irrigation, reduce irrigation, "
                "apply fertilizer, improve drainage, "
                "use disease control, monitor crop closely, "
                "take no action."
            )
        }

    new_score = max(
        0,
        min(100, overall_score + adjustment)
    )

    if new_score >= 75:
        new_risk = "High"
    elif new_score >= 45:
        new_risk = "Medium"
    else:
        new_risk = "Low"

    if new_score < overall_score:
        impact = "Estimated risk decreases"
    elif new_score > overall_score:
        impact = "Estimated risk increases"
    else:
        impact = "No estimated risk change"

    return {
        "status": "success",
        "action": action,
        "original_score": round(overall_score, 1),
        "simulated_score": round(new_score, 1),
        "original_risk": (
            "High" if overall_score >= 75
            else "Medium" if overall_score >= 45
            else "Low"
        ),
        "simulated_risk": new_risk,
        "impact": impact,
        "note": (
            "Simulation is an AI-assisted decision-support estimate "
            "based on predefined risk rules."
        )
    }