import joblib
import pandas as pd

MODEL_PATH = "ml/models/crop_recommendation_model.pkl"

model = joblib.load(MODEL_PATH)

input_data = pd.DataFrame([{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.8,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.9
}])

prediction = model.predict(input_data)[0]

print("Recommended crop:", prediction)
