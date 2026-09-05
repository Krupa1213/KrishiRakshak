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

    # Flood / waterlogging
    if rainfall >= 50 or rain_probability >= 80:
        risks.append("Flood / Waterlogging")

    # Heat stress
    if temperature >= 38:
        risks.append("Heat Stress")

    # Fungal disease
    if humidity >= 85:
        risks.append("Fungal Disease Risk")

    # Strong wind
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

    output_file = (
        "backend/satellite/"
        "fastapi_ndvi_result.tiff"
    )

    try:

        # -----------------------------------------
        # 1. WEATHER DATA
        # -----------------------------------------

        weather = get_weather(
            latitude,
            longitude
        )

        if "error" in weather:
            raise HTTPException(
                status_code=500,
                detail=weather["error"]
            )

        current = weather.get("current", {})
        daily = weather.get("daily", {})

        temperature = float(
            current.get(
                "temperature_2m",
                0
            )
        )

        humidity = float(
            current.get(
                "relative_humidity_2m",
                0
            )
        )

        rainfall = float(
            current.get(
                "precipitation",
                0
            )
        )

        wind_speed = float(
            current.get(
                "wind_speed_10m",
                0
            )
        )

        probability_values = daily.get(
            "precipitation_probability_max",
            [0]
        )

        rain_probability = max(
            probability_values
        )


        # -----------------------------------------
        # 2. WEATHER RISK
        # -----------------------------------------

        weather_risk = calculate_weather_risk(

            temperature,

            humidity,

            rainfall,

            rain_probability,

            wind_speed

        )


        # -----------------------------------------
        # 3. SENTINEL-2 NDVI
        # -----------------------------------------

        start_date = "2026-08-01"
        end_date = "2026-09-05"

        ndvi_data = fetch_ndvi(

            latitude,

            longitude,

            start_date,

            end_date

        )


        # Save TIFF temporarily

        with open(
            output_file,
            "wb"
        ) as file:

            file.write(ndvi_data)


        # -----------------------------------------
        # 4. NDVI ANALYSIS
        # -----------------------------------------

        analysis = analyze_ndvi(
            output_file
        )


        if not analysis["success"]:

            raise HTTPException(
                status_code=500,
                detail=analysis["error"]
            )


        ndvi_risk = analysis["risk_level"]


        # -----------------------------------------
        # 5. COMBINED FARM RISK
        # -----------------------------------------

        farm_risk_result = calculate_farm_risk(

            weather_risk["overall_risk"],

            ndvi_risk

        )


        # -----------------------------------------
        # 6. FINAL RESPONSE
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

                "rain_probability":
                    rain_probability,

                "wind_speed": wind_speed,

                "risk":
                    weather_risk

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

            "farm_risk":
                farm_risk_result

        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)

        )


    finally:

        # Delete temporary NDVI file

        if os.path.exists(output_file):

            try:

                os.remove(output_file)

            except Exception:

                pass
