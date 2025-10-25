from flask import Flask, render_template, request
import requests
from alert_engine import get_aqi_category, send_alert_email


app = Flask(__name__)

API_KEY = "9b97b2b6-09a4-4df6-a783-21cc32df8f6c"
BASE_URL = "http://api.airvisual.com/v2/city"

# Map for cities, their states and country (India)
CITY_STATE_COUNTRY_MAP = {
    "Delhi": ("Delhi", "India"),
    "Mumbai": ("Maharashtra", "India"),
    "Bangalore": ("Karnataka", "India"),
    "Hyderabad": ("Telangana", "India"),
    "Chennai": ("Tamil Nadu", "India"),
    "Kolkata": ("West Bengal", "India"),
    "Pune": ("Maharashtra", "India"),
    "Ahmedabad": ("Gujarat", "India"),
    "Jaipur": ("Rajasthan", "India"),
    "Lucknow": ("Uttar Pradesh", "India"),
    "Mysore": ("Karnataka", "India"),
    "Nagpur": ("Maharashtra", "India"),
    "Indore": ("Madhya Pradesh", "India"),
    "Bhopal": ("Madhya Pradesh", "India"),
    "Patna": ("Bihar", "India"),
    "Raipur": ("Chhattisgarh", "India"),
    "Ranchi": ("Jharkhand", "India"),
    "Thiruvananthapuram": ("Kerala", "India"),
    "Kochi": ("Kerala", "India"),
    "Vijayawada": ("Andhra Pradesh", "India"),
    "Visakhapatnam": ("Andhra Pradesh", "India"),
    "Coimbatore": ("Tamil Nadu", "India"),
    "Madurai": ("Tamil Nadu", "India"),
    "Kanpur": ("Uttar Pradesh", "India"),
    "Varanasi": ("Uttar Pradesh", "India"),
    "Surat": ("Gujarat", "India"),
    "Vadodara": ("Gujarat", "India"),
    "Nashik": ("Maharashtra", "India"),
    "Aurangabad": ("Maharashtra", "India"),
    "Noida": ("Uttar Pradesh", "India"),
    "Gurgaon": ("Haryana", "India"),
    "Chandigarh": ("Chandigarh", "India"),
    "Dehradun": ("Uttarakhand", "India"),
    "Shimla": ("Himachal Pradesh", "India"),
    "Guwahati": ("Assam", "India"),
    "Shillong": ("Meghalaya", "India"),
    "Gangtok": ("Sikkim", "India"),
    "Panaji": ("Goa", "India"),
    "Imphal": ("Manipur", "India"),
    "Agartala": ("Tripura", "India"),
    "Aizawl": ("Mizoram", "India")

}

def fetch_api_data(city, state, country):
    try:
        url = f"{BASE_URL}?city={city}&state={state}&country={country}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data.get("status") == "success":
            pollution_data = data["data"]["current"]["pollution"]
            aqi = pollution_data["aqius"]
            return aqi
        else:
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        city = request.form["city"]
        if city in CITY_STATE_COUNTRY_MAP:
            state, country = CITY_STATE_COUNTRY_MAP[city]
            aqi_val = fetch_api_data(city, state, country)
            if aqi_val is not None:
                category, advice = get_aqi_category(aqi_val)
                send_alert_email(city, aqi_val, category, advice)
                result = {
                    "city": city,
                    "aqi": round(aqi_val, 2),
                    "category": category,
                    "advice": advice,
                    "email_status": "📧 Email alert sent!" if category != "Good" else "✅ No email "
                }
            else:
                result = {"error": f"API data unavailable for {city}"}
        else:
            result = {"error": "City not supported."}
    return render_template("index.html", result=result, cities=list(CITY_STATE_COUNTRY_MAP.keys()))

if __name__ == "__main__":
    app.run(debug=True)

