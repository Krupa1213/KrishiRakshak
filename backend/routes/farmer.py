from fastapi import APIRouter

from backend.models.schemas import (
    Farmer,
    Farm,
    CropData,
    SoilData,
    MarketData,
    GovernmentScheme
)

from backend.database import (
    farmers_collection,
    farms_collection,
    crops_collection,
    soil_collection,
    market_collection,
    government_schemes_collection
)


router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)


# =========================
# FARMER
# =========================

@router.get("/")
def get_farmers():
    farmers = list(
        farmers_collection.find({}, {"_id": 0})
    )
    return farmers


@router.post("/")
def create_farmer(farmer: Farmer):
    farmer_data = farmer.model_dump()

    result = farmers_collection.insert_one(
        farmer_data
    )

    return {
        "message": "Farmer created successfully",
        "farmer_id": str(result.inserted_id)
    }


# =========================
# FARM
# =========================

@router.post("/farm")
def create_farm(farm: Farm):
    farm_data = farm.model_dump()

    farms_collection.insert_one(
        farm_data
    )

    return {
        "message": "Farm created successfully",
        "farm_id": farm.farm_id
    }


@router.get("/farm")
def get_farms():
    farms = list(
        farms_collection.find({}, {"_id": 0})
    )
    return farms


@router.get("/farm/{farm_id}")
def get_farm(farm_id: str):
    farm = farms_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )

    if not farm:
        return {
            "message": "Farm not found"
        }

    return farm


# =========================
# CROP
# =========================

@router.post("/crop")
def create_crop(crop: CropData):
    crop_data = crop.model_dump()

    crops_collection.insert_one(
        crop_data
    )

    return {
        "message": "Crop data created successfully",
        "farm_id": crop.farm_id
    }


@router.get("/crop")
def get_crops():
    crops = list(
        crops_collection.find({}, {"_id": 0})
    )
    return crops


@router.get("/crop/{farm_id}")
def get_crop(farm_id: str):
    crop = crops_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )

    if not crop:
        return {
            "message": "Crop data not found"
        }

    return crop


# =========================
# SOIL
# =========================

@router.post("/soil")
def create_soil(soil: SoilData):
    soil_data = soil.model_dump()

    soil_collection.insert_one(
        soil_data
    )

    return {
        "message": "Soil data created successfully",
        "farm_id": soil.farm_id
    }


@router.get("/soil")
def get_soil():
    soil = list(
        soil_collection.find({}, {"_id": 0})
    )
    return soil


@router.get("/soil/{farm_id}")
def get_soil_by_farm(farm_id: str):
    soil = soil_collection.find_one(
        {"farm_id": farm_id},
        {"_id": 0}
    )

    if not soil:
        return {
            "message": "Soil data not found"
        }

    return soil


# =========================
# MARKET
# =========================

@router.post("/market")
def create_market(market: MarketData):
    market_data = market.model_dump()

    market_collection.insert_one(
        market_data
    )

    return {
        "message": "Market data created successfully",
        "crop_name": market.crop_name
    }


@router.get("/market")
def get_market():
    market = list(
        market_collection.find({}, {"_id": 0})
    )
    return market


@router.get("/market/{crop_name}")
def get_market_by_crop(crop_name: str):
    market = list(
        market_collection.find(
            {"crop_name": crop_name},
            {"_id": 0}
        )
    )

    if not market:
        return {
            "message": "Market data not found"
        }

    return market


# =========================
# GOVERNMENT SCHEMES
# =========================

@router.post("/scheme")
def create_scheme(scheme: GovernmentScheme):
    scheme_data = scheme.model_dump()

    government_schemes_collection.insert_one(
        scheme_data
    )

    return {
        "message": "Government scheme created successfully",
        "scheme_name": scheme.scheme_name
    }


@router.get("/scheme")
def get_schemes():
    schemes = list(
        government_schemes_collection.find({}, {"_id": 0})
    )
    return schemes


@router.get("/scheme/{scheme_name}")
def get_scheme(scheme_name: str):
    scheme = government_schemes_collection.find_one(
        {"scheme_name": scheme_name},
        {"_id": 0}
    )

    if not scheme:
        return {
            "message": "Government scheme not found"
        }

    return scheme