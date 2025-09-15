from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# --- API Key for Weather ---
WEATHER_API_KEY = "cb5eab1352b276cc73182ea4758e8904"

# --- Relief Centers with coordinates ---
relief_centers = {
    "mangalore": [
        {"name": "Town Hall Shelter", "lat": 12.8703, "lng": 74.8806},
        {"name": "Govt School Relief Center", "lat": 12.9156, "lng": 74.8560}
    ],
    "mumbai": [
        {"name": "Bandra Relief Camp", "lat": 19.0544, "lng": 72.8402},
        {"name": "Andheri Govt Shelter", "lat": 19.1197, "lng": 72.8468}
    ],
    "delhi": [
        {"name": "AIIMS Camp", "lat": 28.5667, "lng": 77.2100},
        {"name": "Red Cross Shelter", "lat": 28.6139, "lng": 77.2090}
    ]
}

@app.route("/")
def home():
    return jsonify({"message": "AI Disaster Relief Assistant Backend is running ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # 1️⃣ Weather (any city in India / world supported)
    if "weather" in user_message:
        try:
            city = None
            if "in" in user_message:
                city = user_message.split("in")[-1].strip()
            else:
                city = user_message.replace("weather", "").strip()

            if city:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                res = requests.get(url).json()

                if res.get("cod") != 200:
                    return jsonify({"message": f"⚠️ Could not fetch weather for {city.title()}."})

                temp = res["main"]["temp"]
                desc = res["weather"][0]["description"]
                return jsonify({"message": f"🌦️ Weather in {city.title()}: {temp}°C, {desc}"})
            else:
                return jsonify({"message": "Please mention a city (e.g., 'weather in Bangalore')."})

        except Exception as e:
            return jsonify({"message": f"⚠️ Weather fetch failed. {str(e)}"})

    # 2️⃣ Relief Centers
    elif "relief" in user_message or "shelter" in user_message:
        for city, centers in relief_centers.items():
            if city in user_message:
                return jsonify({
                    "message": f"🏠 Relief centers in {city.title()}:\n" + "\n".join([c['name'] for c in centers]),
                    "relief_centers": centers   # ✅ exact key frontend expects
                })
        return jsonify({"message": "⚠️ No relief center data available for that city yet."})

    # 3️⃣ Default Echo
    else:
        return jsonify({"message": f"🤖 You said: {user_message}"})

if __name__ == "__main__":
    app.run(debug=True)
