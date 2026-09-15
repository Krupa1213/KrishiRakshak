from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import numpy as np
import tensorflow as tf
import os

router = APIRouter(prefix="/disease", tags=["Disease Detection"])

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "models",
    "crop_health_model.keras"
)

# Load disease detection model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Crop disease model loaded successfully!")
except Exception as e:
    model = None
    print(f"Warning: Could not load disease model: {e}")


CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


@router.post("/predict")
async def predict_disease(file: UploadFile = File(...)):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Disease detection model is not available"
        )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file"
        )

    try:
        contents = await file.read()

        image = Image.open(
            __import__("io").BytesIO(contents)
        ).convert("RGB")

        image = image.resize((224, 224))

        image_array = np.array(image, dtype=np.float32)

        image_array = np.expand_dims(image_array, axis=0)

        prediction = model.predict(image_array, verbose=0)[0]

        predicted_index = int(np.argmax(prediction))
        predicted_class = CLASS_NAMES[predicted_index]
        confidence = float(prediction[predicted_index])

        return {
            "prediction": predicted_class,
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )