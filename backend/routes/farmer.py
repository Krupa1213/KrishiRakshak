from fastapi import APIRouter
from backend.models.schemas import Farmer
from backend.database import farmers_collection

router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)


@router.get("/")
def get_farmers():
    farmers = list(farmers_collection.find({}, {"_id": 0}))
    return farmers


@router.post("/")
def create_farmer(farmer: Farmer):
    farmer_data = farmer.model_dump()

    result = farmers_collection.insert_one(farmer_data)

    return {
        "message": "Farmer created successfully",
        "farmer_id": str(result.inserted_id)
    }