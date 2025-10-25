# model_utils.py
import joblib
import pandas as pd
from datetime import datetime

model = joblib.load("models/aqi_model.pkl")

def predict_aqi(input_data):
    today = datetime.now()
    input_data["day"] = today.day
    input_data["month"] = today.month
    input_data["year"] = today.year

    df = pd.DataFrame([input_data])
    predicted_aqi = model.predict(df)[0]
    
    return predicted_aqi
