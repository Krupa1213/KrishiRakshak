from fastapi import APIRouter
from pydantic import BaseModel

from backend.decision_support.decision_engine import generate_decision_support
from backend.decision_support.what_if_simulator import simulate_action


router = APIRouter(
    prefix="/decision-support",
    tags=["Decision Support"]
)


class DecisionRequest(BaseModel):
    overall_risk: str
    weather_risk: str
    ndvi_risk: str
    crop_health_prediction: str | None = None


class WhatIfRequest(BaseModel):
    overall_score: float
    action: str


@router.post("/recommendations")
def get_recommendations(request: DecisionRequest):

    return generate_decision_support(
        overall_risk=request.overall_risk,
        weather_risk=request.weather_risk,
        ndvi_risk=request.ndvi_risk,
        crop_health_prediction=request.crop_health_prediction
    )


@router.post("/what-if")
def what_if_simulation(request: WhatIfRequest):

    return simulate_action(
        overall_score=request.overall_score,
        action=request.action
    )