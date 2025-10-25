# alert_engine.py
import smtplib
from email.message import EmailMessage

def get_aqi_category(aqi):
    aqi = float(aqi)
    if aqi <= 55:
        return "Good", (
            "✅ Air quality is satisfactory.\n"
            "🧘 No health risks.\n"
            "🌿 Ideal for outdoor activities."
        )
    elif aqi <= 100:
        return "Moderate", (
            "⚠️ Air quality is acceptable.\n"
            "🤧 Sensitive individuals (asthmatics, elderly) should limit prolonged outdoor exertion.\n"
            "🟢 You may go outdoors but be cautious if allergic."
        )
    elif aqi <= 150:
        return "Poor", (
            "🚸 Children, elderly, and people with lung/heart conditions should reduce prolonged outdoor activity.\n"
            "😷 Consider wearing a mask outdoors.\n"
            "🏠 Avoid heavy exertion outside."
        )
    elif aqi <= 200:
        return "Very Poor", (
            "❌ Everyone may experience health effects.\n"
            "😩 Breathing discomfort for prolonged outdoor exposure.\n"
            "🏃 Limit physical activities outdoors."
        )
    elif aqi <= 300:
        return "Severe", (
            "🚨 Health alert: serious effects possible for the entire population.\n"
            "🚷 Avoid outdoor activity completely.\n"
            "🪟 Keep windows closed, use air purifiers indoors."
        )
    else:
        return "Hazardous", (
            "☠️ Emergency conditions.\n"
            "🚫 Everyone should stay indoors.\n"
            "💊 Immediate health risks; seek medical attention if symptoms arise.\n"
            "🏥 People with heart/lung diseases: follow doctor’s advice strictly."
        )
def send_alert_email(city, aqi, category, health_advice):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Air Quality Alert for {city}"
        msg["From"] = "appdevelop2003@gmail.com"
        msg["To"] = "likhithahymce@gmail.com"  # 🔁 Replace with actual recipient email
        msg.set_content(f"📍 City: {city}\n🟡 AQI: {aqi}\n🔵 Category: {category}\n📝 Advice: {health_advice}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("appdevelop2003@gmail.com", "vbumhsarzpnsvuwl")  # 🔐 Better to use environment variables
            smtp.send_message(msg)

        print(f"✅ Email alert sent successfully to likhithahymce@gmail.com for {city}")
        return True

    except Exception as e:
        print("❌ Failed to send email:", e)
        return False
