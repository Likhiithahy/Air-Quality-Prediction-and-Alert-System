import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 📥 Load preprocessed dataset
data = pd.read_csv("data/processed.csv")

# ✅ Confirm columns
print("📊 Columns in dataset:", data.columns.tolist())

# 🧼 If 'Date' exists, convert + extract features + drop original
if "Date" in data.columns:
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["day"] = data["Date"].dt.day
    data["month"] = data["Date"].dt.month
    data["year"] = data["Date"].dt.year
    data = data.drop(columns=["Date"])

# ✅ Drop rows with missing values
data = data.dropna()

# 🏷️ Split into Features & Target
X = data.drop(columns=["AQI"])
y = data["AQI"]

# 🎯 Check if any string columns still exist (should be only numeric)
non_numeric = X.select_dtypes(include=["object"]).columns.tolist()
if non_numeric:
    print("⚠️ Dropping non-numeric columns:", non_numeric)
    X = X.drop(columns=non_numeric)

# 🧪 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🌳 Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 💾 Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/aqi_model.pkl")

# 📊 Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# ✅ Output
print("✅ Model trained successfully.")
print(f"📉 RMSE: {rmse:.2f}")
print(f"📉 MAE: {mae:.2f}")
print(f"📈 R² Score: {r2:.2f}")
print("💾 Model saved to models/aqi_model.pkl")
