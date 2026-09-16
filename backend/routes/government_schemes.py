from fastapi import APIRouter

from backend.data.government_schemes import GOVERNMENT_SCHEMES


router = APIRouter(
    prefix="/government-schemes",
    tags=["Government Schemes"]
)


@router.get("/")
def get_government_schemes():
    return {
        "status": "success",
        "schemes": GOVERNMENT_SCHEMES
    }