def generate_recommendations(
    overall_risk,
    weather_risk,
    ndvi_risk,
    crop_health_prediction=None
):
    """
    Generate AI-assisted farm management recommendations
    using existing farm risk indicators.

    This is a prototype decision-support engine.
    It provides recommendations based on risk rules and
    does not claim guaranteed outcomes.
    """

    recommendations = []

    # Overall farm risk
    if overall_risk == "High":
        recommendations.append(
            "Take preventive action immediately and monitor the farm closely."
        )

    elif overall_risk == "Medium":
        recommendations.append(
            "Monitor the farm regularly and take preventive measures where required."
        )

    else:
        recommendations.append(
            "Continue normal crop monitoring and maintain current farm practices."
        )

    # Weather-based recommendations
    if weather_risk == "High":
        recommendations.append(
            "High weather risk detected. Check weather conditions frequently "
            "and protect the crop from excessive rainfall, heat or strong winds."
        )

    elif weather_risk == "Medium":
        recommendations.append(
            "Moderate weather risk detected. Monitor upcoming weather changes "
            "and adjust irrigation or field activities if necessary."
        )

    # Satellite / NDVI recommendations
    if ndvi_risk == "High":
        recommendations.append(
            "Satellite vegetation indicators show high crop stress. "
            "Inspect affected areas for water stress, nutrient deficiency or disease."
        )

    elif ndvi_risk == "Medium":
        recommendations.append(
            "Satellite indicators show moderate vegetation stress. "
            "Inspect the crop and check soil moisture and nutrient conditions."
        )

    # Crop image recommendations
    if crop_health_prediction:
        prediction = crop_health_prediction.lower()

        if "possible crop health issue" in prediction:
            recommendations.append(
                "Crop-image analysis indicates a possible health issue. "
                "Inspect leaves and affected plants and consider expert advice."
            )

        elif "possible crop stress" in prediction:
            recommendations.append(
                "Crop-image analysis indicates possible stress. "
                "Check irrigation, soil moisture and nutrient conditions."
            )

        elif "healthy" in prediction:
            recommendations.append(
                "Crop-image analysis indicates predominantly healthy vegetation. "
                "Continue regular monitoring."
            )

    return recommendations


def generate_decision_support(
    overall_risk,
    weather_risk,
    ndvi_risk,
    crop_health_prediction=None
):
    """
    Generate a complete decision-support response.
    """

    recommendations = generate_recommendations(
        overall_risk=overall_risk,
        weather_risk=weather_risk,
        ndvi_risk=ndvi_risk,
        crop_health_prediction=crop_health_prediction
    )

    return {
        "overall_risk": overall_risk,
        "weather_risk": weather_risk,
        "ndvi_risk": ndvi_risk,
        "crop_health_prediction": crop_health_prediction,
        "recommendations": recommendations
    }