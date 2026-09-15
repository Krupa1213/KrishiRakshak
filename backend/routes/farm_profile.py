from fastapi import APIRouter

from backend.database import (
    farms_collection,
    crops_collection,
    soil_collection,
    market_collection
)


router = APIRouter(
    prefix="/farmers",
    tags=["Farm Profile"]
)


@router.get("/profile/{farm_id}")
def get_farm_profile(farm_id: str):

    farm = farms_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )

    crop = crops_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )

    soil = soil_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )

    market = None

    if crop:
        market = market_collection.find_one(
            {"crop_name": crop.get("crop_name")},
            {"_id": 0}
        )

    return {
        "farm": farm,
        "crop": crop,
        "soil": soil,
        "market": market
    }