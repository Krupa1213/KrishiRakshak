import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("COPERNICUS_CLIENT_ID")
CLIENT_SECRET = os.getenv("COPERNICUS_CLIENT_SECRET")

TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"


def get_access_token():
    """Get an OAuth access token from Copernicus."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Copernicus credentials not found in .env")

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=data, timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]


def fetch_ndvi(latitude, longitude, start_date, end_date):
    """Fetch Sentinel-2 NDVI GeoTIFF for a location and date range."""
    token = get_access_token()
    size = 0.005
    bbox = [longitude - size, latitude - size, longitude + size, latitude + size]

    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["B04", "B08", "SCL"],
            output: { bands: 1, sampleType: "FLOAT32" }
        };
    }
    function evaluatePixel(sample) {
        if ([3, 8, 9, 10].includes(sample.SCL)) return [NaN];
        let denominator = sample.B08 + sample.B04;
        if (denominator === 0) return [NaN];
        return [(sample.B08 - sample.B04) / denominator];
    }
    """

    request_body = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": start_date + "T00:00:00Z", "to": end_date + "T23:59:59Z"},
                    "mosaickingOrder": "leastCC"
                }
            }]
        },
        "output": {
            "width": 100, "height": 100,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
        },
        "evalscript": evalscript
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(PROCESS_URL, headers=headers, json=request_body, timeout=120)
    response.raise_for_status()
    return response.content


if __name__ == "__main__":
    print("🛰️ KrishiRakshak Sentinel-2 NDVI Test")
    latitude, longitude = 12.97194, 77.59369
    start_date, end_date = "2026-08-01", "2026-09-05"

    try:
        ndvi_data = fetch_ndvi(latitude, longitude, start_date, end_date)
        output_file = "ndvi_bengaluru.tiff"
        with open(output_file, "wb") as f:
            f.write(ndvi_data)
        print("✅ NDVI image saved as:", output_file)
    except Exception as e:
        print("❌ NDVI request failed:", e)
