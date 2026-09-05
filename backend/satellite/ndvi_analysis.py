import rasterio
import numpy as np


def analyze_ndvi(file_path):
    """
    Analyze Sentinel-2 NDVI GeoTIFF
    and estimate vegetation condition.
    """

    try:
        with rasterio.open(file_path) as src:
            ndvi = src.read(1)

    except Exception as error:
        return {
            "success": False,
            "error": f"Could not read NDVI file: {error}"
        }

    # Remove NaN and infinite values
    valid_values = ndvi[np.isfinite(ndvi)]

    if len(valid_values) == 0:
        return {
            "success": False,
            "error": "No valid NDVI values found."
        }

    # Calculate statistics
    mean_ndvi = float(np.mean(valid_values))
    minimum_ndvi = float(np.min(valid_values))
    maximum_ndvi = float(np.max(valid_values))

    # Basic vegetation classification
    if mean_ndvi < 0:
        condition = "Water / Non-vegetation"
        risk_level = "High"
        health_score = 0

    elif mean_ndvi < 0.2:
        condition = "Very Low Vegetation"
        risk_level = "High"
        health_score = 25

    elif mean_ndvi < 0.4:
        condition = "Low / Stressed Vegetation"
        risk_level = "Medium"
        health_score = 50

    elif mean_ndvi < 0.6:
        condition = "Moderate / Healthy Vegetation"
        risk_level = "Low"
        health_score = 75

    else:
        condition = "High / Healthy Vegetation"
        risk_level = "Very Low"
        health_score = 90

    return {
        "success": True,
        "mean_ndvi": round(mean_ndvi, 3),
        "minimum_ndvi": round(minimum_ndvi, 3),
        "maximum_ndvi": round(maximum_ndvi, 3),
        "condition": condition,
        "health_score": health_score,
        "risk_level": risk_level
    }


if __name__ == "__main__":

    file_path = "ndvi_bengaluru.tiff"

    print("🛰️ KrishiRakshak NDVI Analysis")
    print("--------------------------------")

    result = analyze_ndvi(file_path)

    if result["success"]:

        print("🌱 Mean NDVI:", result["mean_ndvi"])
        print("📉 Minimum NDVI:", result["minimum_ndvi"])
        print("📈 Maximum NDVI:", result["maximum_ndvi"])
        print("🌾 Vegetation:", result["condition"])
        print("❤️ Health Score:", result["health_score"], "/ 100")
        print("⚠️ Risk Level:", result["risk_level"])

    else:

        print("❌ Analysis failed.")
        print("Error:", result["error"])