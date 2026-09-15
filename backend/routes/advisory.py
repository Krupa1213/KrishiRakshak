from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/advisory", tags=["Farmer Advisory"])


class AdvisoryInput(BaseModel):
    crop: str
    disease: str = "None"
    weather_risk: str = "Low"
    farm_risk: str = "Low"


@router.post("/recommend")
def get_advisory(data: AdvisoryInput):

    advice = []

    # Crop advice
    advice.append(
        f"Continue monitoring your {data.crop} crop regularly."
    )

    # Disease advice
    if data.disease == "Blight":
        advice.append(
            "Blight detected. Remove affected leaves and monitor the crop regularly."
        )
    elif data.disease == "Common_Rust":
        advice.append(
            "Common rust detected. Monitor the leaves and remove severely affected parts."
        )
    elif data.disease == "Gray_Leaf_Spot":
        advice.append(
            "Gray leaf spot detected. Improve field monitoring and remove severely affected leaves."
        )
    elif data.disease != "None" and data.disease != "Healthy":
        advice.append(
            f"Take appropriate preventive measures for {data.disease}."
        )
    else:
        advice.append(
            "No major crop disease has been reported."
        )

    # Weather advice
    if data.weather_risk == "High":
        advice.append(
            "Weather risk is high. Protect the crop from adverse conditions."
        )
    elif data.weather_risk == "Medium":
        advice.append(
            "Weather conditions require monitoring."
        )
    else:
        advice.append(
            "Weather conditions are currently favorable."
        )

    # Farm risk advice
    if data.farm_risk == "High":
        advice.append(
            "Farm risk is high. Inspect the field and take preventive action."
        )
    elif data.farm_risk == "Medium":
        advice.append(
            "Keep monitoring soil, weather and crop health."
        )
    else:
        advice.append(
            "Overall farm conditions are currently stable."
        )

    return {
        "crop": data.crop,
        "advisory": advice
    }