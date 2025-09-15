from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

WEATHER_API_KEY = "cb5eab1352b276cc73182ea4758e8904"

# Relief centers (demo)
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

# Major cities list for default weather display
major_cities = ["mumbai", "delhi", "bangalore", "chennai", "kolkata", "hyderabad", "pune", "ahmedabad", "jaipur", "mangalore"]

@app.route("/")
def home():
    return jsonify({"message": "AI Disaster Relief Assistant Backend is running ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()

    # 1️⃣ Weather
    if "weather" in user_message:
        words = user_message.split()
        # Try to detect city mentioned after 'weather' or 'in'
        city = None
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city = words[city_index]
        elif len(words) > 1:
            city = words[1]

        weather_messages = []

        # If city mentioned → fetch weather for that city
        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                res = requests.get(url).json()
                if res.get("cod") != 200:
                    weather_messages.append(f"⚠️ Could not fetch weather for {city.title()}.")
                else:
                    temp = res["main"]["temp"]
                    desc = res["weather"][0]["description"]
                    weather_messages.append(f"🌦️ {city.title()}: {temp}°C, {desc}")
            except Exception as e:
                weather_messages.append(f"⚠️ Weather fetch failed for {city.title()}: {str(e)}")
        else:
            # No city → fetch for all major cities
            for c in major_cities:
                try:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={c}&appid={WEATHER_API_KEY}&units=metric"
                    res = requests.get(url).json()
                    if res.get("cod") != 200:
                        weather_messages.append(f"⚠️ Could not fetch weather for {c.title()}.")
                    else:
                        temp = res["main"]["temp"]
                        desc = res["weather"][0]["description"]
                        weather_messages.append(f"🌦️ {c.title()}: {temp}°C, {desc}")
                except Exception as e:
                    weather_messages.append(f"⚠️ Weather fetch failed for {c.title()}: {str(e)}")

        return jsonify({"message": "\n".join(weather_messages), "centers": []})

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
