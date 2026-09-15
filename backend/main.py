from fastapi import FastAPI
from pydantic import BaseModel
from backend import farm_risk_api  # import your risk calculation logic

app = FastAPI()

# Define the request body schema
class FarmData(BaseModel):
    farm_id: str
    farmer_name: str
    latitude: float
    longitude: float
    area_acres: float
    crop: str
    crop_variety: str
    sowing_date: str
    soil_type: str
    irrigation_type: str
    growth_stage: str

@app.get("/")
def root():
    return {"message": "KrishiRakshak API is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Change farm risk to POST
@app.post("/farm/risk")
def farm_risk(data: FarmData):
    # Call your risk calculation function
    result = farm_risk_api.calculate_risk(
        latitude=data.latitude,
        longitude=data.longitude,
        crop=data.crop,
        area=data.area_acres
    )
    return {
        "farm_id": data.farm_id,
        "farmer_name": data.farmer_name,
        "risk_result": result
    }
