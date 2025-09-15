from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# --- Relief Centers (demo DB) ---
relief_centers = {
    "mangalore": [
        {"name": "Town Hall Shelter", "lat": 12.8703, "lon": 74.8806},
        {"name": "Govt School Relief Center", "lat": 12.9156, "lon": 74.8559}
    ],
    "mumbai": [
        {"name": "Bandra Relief Camp", "lat": 19.0596, "lon": 72.8295},
        {"name": "Andheri Govt Shelter", "lat": 19.1197, "lon": 72.8468}
    ],
    "delhi": [
        {"name": "AIIMS Camp", "lat": 28.5672, "lon": 77.2100},
        {"name": "Red Cross Shelter", "lat": 28.6139, "lon": 77.2090}
    ]
}

# ✅ OpenWeather API Key
WEATHER_API_KEY = "cb5eab1352b276cc73182ea4758e8904"

@app.route("/")
def home():
    return jsonify({"message": "AI Disaster Relief Assistant Backend is running ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Weather info
    if "weather" in user_message:
        for city in relief_centers.keys():
            if city in user_message:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                try:
                    res = requests.get(url).json()
                    if res.get("cod") != 200:
                        return jsonify({"message": f"Sorry, couldn't fetch weather for {city.title()}."})
                    weather = res["weather"][0]["description"]
                    temp = res["main"]["temp"]
                    return jsonify({"message": f"🌤 Weather in {city.title()}: {weather}, {temp}°C"})
                except Exception as e:
                    return jsonify({"message": f"Error fetching weather: {str(e)}"})
        return jsonify({"message": "Please mention a valid city for weather (e.g., Mumbai, Delhi, Mangalore)."})

    # Relief centers
    elif "relief" in user_message or "shelter" in user_message:
        for city, centers in relief_centers.items():
            if city in user_message:
                return jsonify({
                    "message": f"Here are nearby relief centers in {city.title()}:",
                    "centers": centers
                })
        return jsonify({"message": "Sorry, I don’t have shelter data for that location yet."})

    # Default echo
    else:
        return jsonify({"message": f"You said: {user_message}"})

@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "").lower()
    if city in relief_centers:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            res = requests.get(url).json()
            if res.get("cod") != 200:
                return jsonify({"message": f"Sorry, couldn't fetch weather for {city.title()}."})
            weather = res["weather"][0]["description"]
            temp = res["main"]["temp"]
            return jsonify({"message": f"🌤 Weather in {city.title()}: {weather}, {temp}°C"})
        except Exception as e:
            return jsonify({"message": f"Error fetching weather: {str(e)}"})
    return jsonify({"message": "Please provide a valid city (Mumbai, Delhi, Mangalore)."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
