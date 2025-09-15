from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "cb5eab1352b276cc73182ea4758e8904"

relief_centers = {
    "mangalore": ["Town Hall Shelter", "Govt School Relief Center"],
    "delhi": ["AIIMS Camp", "Red Cross Shelter"],
    "mumbai": ["Bandra Relief Camp", "Andheri Govt Shelter"]
}

@app.route("/")
def home():
    return jsonify({"message": "AI Disaster Relief Assistant Backend is running ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Weather
    if "weather" in user_message:
        city = None
        for c in ["mangalore", "mumbai", "delhi"]:
            if c in user_message:
                city = c
                break
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                data = response.json()
                if data.get("main"):
                    temp = data["main"]["temp"]
                    weather = data["weather"][0]["description"]
                    return jsonify({"message": f"Weather in {city.title()}: {temp}°C, {weather}"})
                else:
                    return jsonify({"message": "Sorry, I couldn’t fetch weather information."})
            except:
                return jsonify({"message": "Weather service unavailable."})
        else:
            return jsonify({"message": "Please ask weather for a supported city (Mangalore, Mumbai, Delhi)."})

    # Relief Centers
    elif "relief" in user_message or "shelter" in user_message:
        for city, centers in relief_centers.items():
            if city in user_message:
                return jsonify({"message": f"Here are nearby relief centers in {city.title()}: {', '.join(centers)}"})
        return jsonify({"message": "Sorry, no relief center data available for that location."})

    # Default
    else:
        return jsonify({"message": f"You said: {user_message}"})

if __name__ == "__main__":
    app.run(debug=True)
