import smtplib
from email.mime.text import MIMEText

SENDER = "sender@example.com"
PASSWORD = "your_password_here"  # 🔐 Use environment variables for security
RECEIVER = "recipient@example.com"  # 🔁 Replace with actual recipient email

def send_alert_email(city, aqi, category, health_tip):
    try:
        msg = MIMEText(f"""
        City: {city}
        AQI: {aqi}
        Category: {category}
        Advice: {health_tip}
        """)
        msg['Subject'] = f"🚨 AQI Alert: {category} in {city}"
        msg['From'] = SENDER
        msg['To'] = RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())

        return "✅ Sent"
    except Exception as e:
        return f"❌ Failed: {str(e)}"
