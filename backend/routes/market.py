from fastapi import APIRouter

router = APIRouter(prefix="/market", tags=["Market Prices"])


@router.get("/price")
def get_market_price():
    return {
        "crop": "Wheat",
        "price": 2450,
        "unit": "Quintal",
        "market": "Vadodara",
        "status": "Available"
    }