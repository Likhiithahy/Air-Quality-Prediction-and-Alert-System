import joblib
import pandas as pd
from datetime import datetime
import numpy as np
import pickle  # In case you want to use pickle-based models

def fetch_city_aqi_data(city):
    # Sample input data (Replace with real-time data as needed)
    input_data = {
        "PM2.5": 180,
        "PM10": 200,
        "NO": 50,
        "NO2": 70,
        "NOx": 120,
        "NH3": 30,
        "CO": 1.2,
        "SO2": 15,
        "O3": 45,
        "Benzene": 5,
        "Toluene": 20,
    }

    today = datetime.now()
    input_data["day"] = today.day
    input_data["month"] = today.month
    input_data["year"] = today.year

    # Load your trained model (joblib version)
    model = joblib.load("models/aqi_model.pkl")
    df = pd.DataFrame([input_data])
    predicted_aqi = model.predict(df)[0]

    # Category and health advice
    if predicted_aqi <= 50:
        category = "Good"
        health_advice = "✅ Air quality is satisfactory, and air pollution poses little or no risk."
    elif predicted_aqi <= 100:
        category = "Fair"
        health_advice = "🔅 Air quality is acceptable. Sensitive people may feel minor irritation."
    elif predicted_aqi <= 200:
        category = "Moderate"
        health_advice = "⚠️ People with respiratory issues should reduce outdoor exertion."
    elif predicted_aqi <= 300:
        category = "Poor"
        health_advice = "🚨 Avoid outdoor activities. Wear masks if necessary."
    elif predicted_aqi <= 400:
        category = "Very Poor"
        health_advice = "❗ Serious health effects possible. Stay indoors."
    else:
        category = "Severe"
        health_advice = "☠️ Hazardous air quality. Remain indoors and use air purifiers."

    return round(predicted_aqi), category, health_advice


# Optional additional function if you want to use pickle-based model directly with raw features
def predict_aqi(features):
    """
    Predict AQI index from input features list (e.g., [CO, NO, NO2, O3, SO2])
    This is a standalone function using 'pickle' instead of 'joblib'.
    Only use if you prefer manual feature input.
    """
    with open("aqi_model.pkl", "rb") as f:
        model = pickle.load(f)

    features = np.array(features).reshape(1, -1)
    predicted_aqi = model.predict(features)[0]
    return round(predicted_aqi)
