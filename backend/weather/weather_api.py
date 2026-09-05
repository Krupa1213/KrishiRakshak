from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

from weather_service import get_coordinates, get_weather


class WeatherAPIHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status_code=200):

        self.send_response(status_code)

        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )

    def do_OPTIONS(self):
        self.send_response(200)

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

    def do_GET(self):

        parsed_url = urlparse(self.path)

        if parsed_url.path != "/weather":

            self.send_json(
                {
                    "error": "Invalid endpoint. Use /weather?location=Bengaluru"
                },
                404
            )

            return

        query = parse_qs(parsed_url.query)

        location = query.get("location", [None])[0]

        if not location:

            self.send_json(
                {
                    "error": "Please provide a location."
                },
                400
            )

            return

        coordinates = get_coordinates(location)

        if not coordinates:

            self.send_json(
                {
                    "error": "Location not found."
                },
                404
            )

            return

        weather = get_weather(
            coordinates["latitude"],
            coordinates["longitude"]
        )

        response = {
            "location": coordinates,
            "weather": weather
        }

        self.send_json(response)


if __name__ == "__main__":

    server_address = ("127.0.0.1", 8000)

    server = HTTPServer(
        server_address,
        WeatherAPIHandler
    )

    print("🌦️ KrishiRakshak Weather API started!")
    print("Server running at: http://127.0.0.1:8000")
    print("Example:")
    print("http://127.0.0.1:8000/weather?location=Bengaluru")

    server.serve_forever()