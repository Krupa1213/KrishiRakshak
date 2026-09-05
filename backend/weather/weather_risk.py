def calculate_weather_risk(
    temperature,
    humidity,
    rainfall,
    rain_probability,
    wind_speed
):
    """
    Estimate basic weather-related farm risk.
    This is a prototype rule-based model.
    """

    risks = []

    # Heavy rainfall risk
    if rainfall >= 50 or rain_probability >= 80:
        risks.append("Flood / Waterlogging")

    # High temperature risk
    if temperature >= 38:
        risks.append("Heat Stress")

    # High humidity risk
    if humidity >= 85:
        risks.append("Fungal Disease Risk")

    # Strong wind risk
    if wind_speed >= 40:
        risks.append("Strong Wind")

    # Overall risk
    if len(risks) >= 2:
        overall_risk = "High"

    elif len(risks) == 1:
        overall_risk = "Medium"

    else:
        overall_risk = "Low"

    return {
        "overall_risk": overall_risk,
        "identified_risks": risks
    }


if __name__ == "__main__":

    print("🌦️ KrishiRakshak Weather Risk Detection")
    print("----------------------------------------")

    result = calculate_weather_risk(
        temperature=36,
        humidity=88,
        rainfall=20,
        rain_probability=85,
        wind_speed=18
    )

    print("⚠️ Overall Risk:", result["overall_risk"])

    print("🔍 Identified Risks:")

    if result["identified_risks"]:
        for risk in result["identified_risks"]:
            print(" -", risk)
    else:
        print(" - No major weather risk detected")