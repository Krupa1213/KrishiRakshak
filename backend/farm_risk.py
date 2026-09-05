def calculate_farm_risk(weather_risk, ndvi_risk):
    """
    Combine weather risk and satellite vegetation risk
    into an overall farm risk score.

    Prototype rule-based model.
    """

    risk_scores = {
        "Low": 25,
        "Medium": 60,
        "High": 90
    }

    weather_score = risk_scores.get(weather_risk, 60)
    ndvi_score = risk_scores.get(ndvi_risk, 60)

    # Weather has slightly higher weight
    overall_score = (
        weather_score * 0.6 +
        ndvi_score * 0.4
    )

    if overall_score >= 75:
        overall_risk = "High"

    elif overall_score >= 45:
        overall_risk = "Medium"

    else:
        overall_risk = "Low"

    return {
        "weather_risk": weather_risk,
        "ndvi_risk": ndvi_risk,
        "weather_score": weather_score,
        "ndvi_score": ndvi_score,
        "overall_score": round(overall_score, 1),
        "overall_risk": overall_risk
    }


if __name__ == "__main__":

    print("🌾 KrishiRakshak Farm Risk Assessment")
    print("-------------------------------------")

    # Example values from our two modules
    weather_risk = "High"
    ndvi_risk = "Medium"

    result = calculate_farm_risk(
        weather_risk,
        ndvi_risk
    )

    print("🌦️ Weather Risk:", result["weather_risk"])
    print("🛰️ NDVI Risk:", result["ndvi_risk"])

    print("📊 Weather Score:", result["weather_score"])
    print("🌱 NDVI Score:", result["ndvi_score"])

    print("⚠️ Overall Farm Risk Score:",
          result["overall_score"], "/ 100")

    print("🚨 Overall Farm Risk:",
          result["overall_risk"])