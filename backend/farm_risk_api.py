from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from farm_risk import calculate_farm_risk


class FarmRiskAPIHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status_code=200):

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )

    def do_OPTIONS(self):

        self.send_response(200)

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

    def do_GET(self):

        print("REQUEST RECEIVED:", self.path)

        parsed_url = urlparse(self.path)

        if parsed_url.path != "/farm-risk":

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Invalid endpoint. "
                        "Use /farm-risk?weather_risk=High&ndvi_risk=Medium"
                    )
                },
                404
            )

            return

        query = parse_qs(parsed_url.query)

        weather_risk = query.get(
            "weather_risk",
            [None]
        )[0]

        ndvi_risk = query.get(
            "ndvi_risk",
            [None]
        )[0]

        if weather_risk is None or ndvi_risk is None:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Please provide weather_risk "
                        "and ndvi_risk."
                    )
                },
                400
            )

            return

        valid_risks = [
            "Low",
            "Medium",
            "High"
        ]

        if weather_risk not in valid_risks:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "weather_risk must be Low, "
                        "Medium, or High."
                    )
                },
                400
            )

            return

        if ndvi_risk not in valid_risks:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "ndvi_risk must be Low, "
                        "Medium, or High."
                    )
                },
                400
            )

            return

        try:

            result = calculate_farm_risk(
                weather_risk,
                ndvi_risk
            )

            response = {
                "success": True,
                "farm_risk": result
            }

            self.send_json(response)

            print("✅ Farm risk calculated.")

        except Exception as error:

            print("❌ Farm Risk API Error:", error)

            self.send_json(
                {
                    "success": False,
                    "error": str(error)
                },
                500
            )


if __name__ == "__main__":

    server_address = (
        "127.0.0.1",
        8002
    )

    server = HTTPServer(
        server_address,
        FarmRiskAPIHandler
    )

    print("🌾 KrishiRakshak Farm Risk API started!")
    print("---------------------------------------")

    print(
        "Server running at:"
    )

    print(
        "http://127.0.0.1:8002"
    )

    print("\nExample:")

    print(
        "http://127.0.0.1:8002/"
        "farm-risk?weather_risk=High&ndvi_risk=Medium"
    )

    server.serve_forever()