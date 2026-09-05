from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import os

from satellite_service import fetch_ndvi
from ndvi_analysis import analyze_ndvi


class NDVIAPIHandler(BaseHTTPRequestHandler):

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

        # Check endpoint
        if parsed_url.path != "/ndvi":

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Invalid endpoint. "
                        "Use /ndvi?latitude=12.97&longitude=77.59"
                    )
                },
                404
            )

            return

        # Get query parameters
        query = parse_qs(parsed_url.query)

        latitude = query.get(
            "latitude",
            [None]
        )[0]

        longitude = query.get(
            "longitude",
            [None]
        )[0]

        # Check parameters
        if latitude is None or longitude is None:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Please provide latitude "
                        "and longitude."
                    )
                },
                400
            )

            return

        # Convert coordinates
        try:

            latitude = float(latitude)
            longitude = float(longitude)

        except ValueError:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Latitude and longitude "
                        "must be numbers."
                    )
                },
                400
            )

            return

        # Validate latitude
        if not -90 <= latitude <= 90:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Latitude must be between "
                        "-90 and 90."
                    )
                },
                400
            )

            return

        # Validate longitude
        if not -180 <= longitude <= 180:

            self.send_json(
                {
                    "success": False,
                    "error": (
                        "Longitude must be between "
                        "-180 and 180."
                    )
                },
                400
            )

            return

        # Date range
        start_date = "2026-08-01"
        end_date = "2026-09-05"

        # Temporary TIFF file
        output_file = "ndvi_api_result.tiff"

        try:

            print("🛰️ Requesting Sentinel-2 NDVI...")

            # Get NDVI from Sentinel-2
            ndvi_data = fetch_ndvi(
                latitude,
                longitude,
                start_date,
                end_date
            )

            # Save NDVI TIFF
            with open(
                output_file,
                "wb"
            ) as file:

                file.write(ndvi_data)

            print("✅ NDVI data received.")

            # Analyze NDVI
            analysis = analyze_ndvi(
                output_file
            )

            # Check analysis
            if not analysis["success"]:

                self.send_json(
                    {
                        "success": False,
                        "error": analysis["error"]
                    },
                    500
                )

                return

            # Prepare response
            result = {

                "success": True,

                "location": {

                    "latitude": latitude,

                    "longitude": longitude
                },

                "date_range": {

                    "start": start_date,

                    "end": end_date
                },

                "ndvi": {

                    "mean":
                        analysis["mean_ndvi"],

                    "minimum":
                        analysis["minimum_ndvi"],

                    "maximum":
                        analysis["maximum_ndvi"],

                    "health_score":
                        analysis["health_score"],

                    "risk_level":
                        analysis["risk_level"]
                },

                "vegetation_condition":
                    analysis["condition"]
            }

            # Send response
            self.send_json(result)

            print("✅ NDVI analysis completed.")

        except Exception as error:

            print(
                "❌ NDVI API Error:",
                error
            )

            self.send_json(
                {
                    "success": False,
                    "error": str(error)
                },
                500
            )

        finally:

            # Delete temporary file
            if os.path.exists(output_file):

                try:
                    os.remove(output_file)

                except Exception:
                    pass


if __name__ == "__main__":

    server_address = (
        "127.0.0.1",
        8001
    )

    server = HTTPServer(
        server_address,
        NDVIAPIHandler
    )

    print(
        "🛰️ KrishiRakshak NDVI API started!"
    )

    print(
        "Server running at:"
    )

    print(
        "http://127.0.0.1:8001"
    )

    print("\nExample:")

    print(
        "http://127.0.0.1:8001/"
        "ndvi?latitude=12.97194&longitude=77.59369"
    )

    server.serve_forever()