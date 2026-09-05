from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

router = APIRouter(prefix="/crop", tags=["Crop Recommendation"])

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "models",
    "crop_recommendation_model.pkl"
)

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load crop model: {e}")


class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


@router.post("/recommend")
def recommend_crop(data: CropInput):
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Crop recommendation model is not available"
        )

    input_data = pd.DataFrame([{
        "N": data.N,
        "P": data.P,
        "K": data.K,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ph": data.ph,
        "rainfall": data.rainfall
    }])

    prediction = model.predict(input_data)[0]

    return {
        "recommended_crop": prediction
    }
