from PIL import Image
import io


def analyze_crop_image(image_bytes: bytes):
    """
    Basic crop-image health analysis.
    This is a prototype for the KrishiRakshak AI system.
    """

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        width, height = image.size

        if width < 100 or height < 100:
            return {
                "status": "error",
                "message": "Image is too small. Please upload a clearer crop image."
            }

        # Calculate average RGB values
        pixels = list(image.resize((100, 100)).getdata())

        avg_r = sum(pixel[0] for pixel in pixels) / len(pixels)
        avg_g = sum(pixel[1] for pixel in pixels) / len(pixels)
        avg_b = sum(pixel[2] for pixel in pixels) / len(pixels)

        # Simple prototype health indicator
        green_ratio = avg_g / max(avg_r + avg_g + avg_b, 1)

        if green_ratio >= 0.40:
            prediction = "Healthy / Green Vegetation"
            confidence = 0.70
            recommendation = (
                "Crop appears predominantly green. "
                "Continue regular monitoring and maintain proper irrigation."
            )
        elif green_ratio >= 0.32:
            prediction = "Possible Crop Stress"
            confidence = 0.60
            recommendation = (
                "Possible crop stress detected. "
                "Check soil moisture, nutrient levels and weather conditions."
            )
        else:
            prediction = "Possible Crop Health Issue"
            confidence = 0.55
            recommendation = (
                "The image shows limited green vegetation. "
                "Inspect the crop for disease, nutrient deficiency or water stress."
            )

        return {
            "status": "success",
            "prediction": prediction,
            "confidence": confidence,
            "recommendation": recommendation,
            "image_size": {
                "width": width,
                "height": height
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not analyze image: {str(e)}"
        }