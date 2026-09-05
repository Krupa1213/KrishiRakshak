import json
from urllib.request import urlopen
from urllib.parse import urlencode


def get_weather(latitude, longitude):
    """
    Get current weather and forecast for a farm location.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "forecast_days": 3,
        "timezone": "auto"
    }

    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)

    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode())

        return data

    except Exception as error:
        return {
            "error": str(error)
        }


if __name__ == "__main__":

    # Example: Bengaluru coordinates
    latitude = 12.9716
    longitude = 77.5946

    weather = get_weather(latitude, longitude)

    print(json.dumps(weather, indent=4))