from fastapi import APIRouter
from backend.models.schemas import Farmer, Farm
from backend.database import farmers_collection, farms_collection
from backend import farm_risk_api  # import your risk logic

router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)

# Get all farmers
@router.get("/")
def get_farmers():
    farmers = list(farmers_collection.find({}, {"_id": 0}))
    return farmers

# Create a farmer
@router.post("/")
def create_farmer(farmer: Farmer):
    farmer_data = farmer.model_dump()
    result = farmers_collection.insert_one(farmer_data)
    return {
        "message": "Farmer created successfully",
        "farmer_id": str(result.inserted_id)
    }

# Create a farm (with risk calculation)
@router.post("/farm")
def create_farm(farm: Farm):
    farm_data = farm.model_dump()
    farms_collection.insert_one(farm_data)

    # Call your risk calculation logic
    risk_result = farm_risk_api.calculate_risk(
        latitude=farm.latitude,
        longitude=farm.longitude,
        crop=farm.crop,
        area=farm.area_acres
    )

    return {
        "message": "Farm created successfully",
        "farm_id": farm.farm_id,
        "risk_result": risk_result
    }

# Get all farms
@router.get("/farm")
def get_farms():
    farms = list(farms_collection.find({}, {"_id": 0}))
    return farms

# Get a specific farm
@router.get("/farm/{farm_id}")
def get_farm(farm_id: str):
    farm = farms_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )
    if not farm:
        return {"message": "Farm not found"}
    return farm
