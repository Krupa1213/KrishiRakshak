from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.crop_health.disease_detector import analyze_crop_image


router = APIRouter(
    prefix="/crop-health",
    tags=["Crop Health"]
)


@router.post("/analyze")
async def analyze_crop_health(
    file: UploadFile = File(...)
):
    """
    Analyze an uploaded crop image
    and return crop-health information.
    """

    # Check file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid crop image."
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )

    result = analyze_crop_image(image_bytes)

    return result