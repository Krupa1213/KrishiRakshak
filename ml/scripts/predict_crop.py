import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array

MODEL_PATH = "ml/models/crop_health_model.keras"
IMG_SIZE = (224, 224)


def predict_crop(image_path):

    if not os.path.exists(MODEL_PATH):
        return {
            "status": "model_not_available",
            "message": "Crop health model has not been trained yet."
        }

    model = tf.keras.models.load_model(MODEL_PATH)

    image = load_img(image_path, target_size=IMG_SIZE)
    image = img_to_array(image)

    # Match the preprocessing used during training
    image = (image / 127.5) - 1
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)

    class_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "status": "success",
        "class_index": class_index,
        "confidence": round(confidence, 4)
    }


if __name__ == "__main__":
    print("KrishiRakshak Crop Health Prediction")
    print("Waiting for trained model and dataset...")