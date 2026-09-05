def calculate_ndvi_change(previous_ndvi, current_ndvi):
    """
    Calculate the change in NDVI between
    two observations.
    """

    change = current_ndvi - previous_ndvi

    if change > 0.10:
        trend = "Significant Improvement"
        risk = "Low"

    elif change > 0.03:
        trend = "Improving"
        risk = "Low"

    elif change >= -0.03:
        trend = "Stable"
        risk = "Medium"

    elif change >= -0.10:
        trend = "Declining"
        risk = "Medium"

    else:
        trend = "Significant Decline"
        risk = "High"

    return {
        "previous_ndvi": round(previous_ndvi, 3),
        "current_ndvi": round(current_ndvi, 3),
        "change": round(change, 3),
        "trend": trend,
        "risk_level": risk
    }


if __name__ == "__main__":

    print("🛰️ KrishiRakshak NDVI Change Detection")
    print("----------------------------------------")

    # Example values for testing
    previous_ndvi = 0.62
    current_ndvi = 0.43

    result = calculate_ndvi_change(
        previous_ndvi,
        current_ndvi
    )

    print("🌱 Previous NDVI:", result["previous_ndvi"])
    print("🌱 Current NDVI:", result["current_ndvi"])
    print("📊 NDVI Change:", result["change"])
    print("📈 Vegetation Trend:", result["trend"])
    print("⚠️ Risk Level:", result["risk_level"])