from fastapi import APIRouter, HTTPException
from backend.weather.weather_service import get_weather
from backend.satellite.satellite_service import fetch_ndvi
from backend.satellite.ndvi_analysis import analyze_ndvi
from backend.farm_risk import calculate_farm_risk

import os


router = APIRouter(
    prefix="/farm",
    tags=["Weather & Satellite"]
)


def calculate_weather_risk(
    temperature,
    humidity,
    rainfall,
    rain_probability,
    wind_speed
):
    """
    Basic prototype weather risk calculation.
    """

    risks = []

    if rainfall >= 50 or rain_probability >= 80:
        risks.append("Flood / Waterlogging")

    if temperature >= 38:
        risks.append("Heat Stress")

    if humidity >= 85:
        risks.append("Fungal Disease Risk")

    if wind_speed >= 40:
        risks.append("Strong Wind")

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


@router.get("/risk")
def farm_risk(
    latitude: float,
    longitude: float
):

    try:

        # -----------------------------------------
        # 1. WEATHER
        # -----------------------------------------

        weather = get_weather(
            latitude,
            longitude
        )

        current = weather["current"]
        daily = weather["daily"]

        temperature = float(
            current["temperature_2m"]
        )

        humidity = float(
            current["relative_humidity_2m"]
        )

        rainfall = float(
            current["precipitation"]
        )

        wind_speed = float(
            current["wind_speed_10m"]
        )

        rain_probability = max(
            daily["precipitation_probability_max"]
        )


        weather_risk = calculate_weather_risk(
            temperature,
            humidity,
            rainfall,
            rain_probability,
            wind_speed
        )


        # -----------------------------------------
        # 2. SATELLITE / NDVI
        # -----------------------------------------

        start_date = "2026-08-01"
        end_date = "2026-09-05"

        ndvi_data = fetch_ndvi(
            latitude,
            longitude,
            start_date,
            end_date
        )


        output_file = (
            "backend/satellite/"
            "fastapi_ndvi_result.tiff"
        )


        with open(
            output_file,
            "wb"
        ) as file:

            file.write(ndvi_data)


        analysis = analyze_ndvi(
            output_file
        )


        # Remove temporary file

        if os.path.exists(output_file):

            os.remove(output_file)


        if not analysis["success"]:

            raise HTTPException(
                status_code=500,
                detail=analysis["error"]
            )


        ndvi_risk = analysis["risk_level"]


        # -----------------------------------------
        # 3. COMBINED FARM RISK
        # -----------------------------------------

        farm_risk_result = calculate_farm_risk(
            weather_risk["overall_risk"],
            ndvi_risk
        )


        # -----------------------------------------
        # 4. FINAL RESPONSE
        # -----------------------------------------

        return {

            "success": True,

            "location": {
                "latitude": latitude,
                "longitude": longitude
            },

            "weather": {

                "temperature": temperature,

                "humidity": humidity,

                "rainfall": rainfall,

                "rain_probability": rain_probability,

                "wind_speed": wind_speed,

                "risk": weather_risk

            },

            "satellite": {

                "mean_ndvi":
                    analysis["mean_ndvi"],

                "minimum_ndvi":
                    analysis["minimum_ndvi"],

                "maximum_ndvi":
                    analysis["maximum_ndvi"],

                "vegetation_condition":
                    analysis["condition"],

                "health_score":
                    analysis["health_score"],

                "risk_level":
                    ndvi_risk

            },

            "farm_risk": farm_risk_result

        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
