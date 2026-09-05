import json
from urllib.request import urlopen
from urllib.parse import urlencode


def get_coordinates(location):
    """
    Convert a city or place name into latitude and longitude.
    """

    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    url = "https://geocoding-api.open-meteo.com/v1/search?" + urlencode(params)

    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode())

        if "results" not in data or not data["results"]:
            return None

        result = data["results"][0]

        return {
            "name": result["name"],
            "country": result.get("country"),
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }

    except Exception as error:
        print("Geocoding error:", error)
        return None


def get_weather(latitude, longitude):
    """
    Get current weather and 3-day forecast for a farm location.
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

    # Enter the city or farm location here
    location = "Bengaluru"

    # Convert location name to coordinates
    coordinates = get_coordinates(location)

    if coordinates:

        print("Location:", coordinates["name"])
        print("Country:", coordinates["country"])
        print("Latitude:", coordinates["latitude"])
        print("Longitude:", coordinates["longitude"])

        # Get weather using the coordinates
        weather = get_weather(
            coordinates["latitude"],
            coordinates["longitude"]
        )

        print("\nWeather Data:")
        print(json.dumps(weather, indent=4))

    else:
        print("Location not found.")