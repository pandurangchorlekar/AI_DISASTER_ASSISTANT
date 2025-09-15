from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# --- API Key for Weather ---
WEATHER_API_KEY = "cb5eab1352b276cc73182ea4758e8904"

# --- Relief Centers with coordinates ---
relief_centers = {
    "mangalore": [
        {"name": "Town Hall Shelter", "lat": 12.8703, "lon": 74.8806},
        {"name": "Govt School Relief Center", "lat": 12.9156, "lon": 74.8560}
    ],
    "mumbai": [
        {"name": "Bandra Relief Camp", "lat": 19.0544, "lon": 72.8402},
        {"name": "Andheri Govt Shelter", "lat": 19.1197, "lon": 72.8468}
    ],
    "delhi": [
        {"name": "AIIMS Camp", "lat": 28.5667, "lon": 77.2100},
        {"name": "Red Cross Shelter", "lat": 28.6139, "lon": 77.2090}
    ]
}

@app.route("/")
def home():
    return jsonify({"message": "AI Disaster Relief Assistant Backend is running ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # 1️⃣ Weather
    if "weather" in user_message:
        weather_cities = []

        # Check if a city is mentioned
        for city in relief_centers.keys():
            if city in user_message:
                weather_cities = [city]
                break

        # If no city mentioned, show weather for all cities
        if not weather_cities:
            weather_cities = list(relief_centers.keys())

        messages = []
        for city in weather_cities:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                res = requests.get(url).json()

                if res.get("cod") != 200:
                    messages.append(f"⚠️ Could not fetch weather for {city.title()}.")
                    continue

                temp = res["main"]["temp"]
                desc = res["weather"][0]["description"]
                messages.append(f"🌦️ {city.title()}: {temp}°C, {desc}")
            except Exception as e:
                messages.append(f"⚠️ Weather fetch failed for {city.title()}. {str(e)}")

        return jsonify({"message": "\n".join(messages), "centers": []})

    # 2️⃣ Relief Centers
    elif "relief" in user_message or "shelter" in user_message:
        for city, centers in relief_centers.items():
            if city in user_message:
                return jsonify({
                    "message": f"🏠 Relief centers in {city.title()}:",
                    "centers": centers
                })
        return jsonify({"message": "⚠️ No relief center data available for that city yet.", "centers": []})

    # 3️⃣ Default Echo
    else:
        return jsonify({"message": f"🤖 You said: {user_message}", "centers": []})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
