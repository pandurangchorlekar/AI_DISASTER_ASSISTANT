import React, { useState } from "react";
import "./App.css";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Marker Icon Fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [centers, setCenters] = useState([]);

  const backendURL = "https://ai-disaster-assistant-2.onrender.com";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { sender: "user", text: input };
    setMessages([...messages, newMessage]);

    try {
      let endpoint = "/chat";
      let method = "POST";
      let body = JSON.stringify({ message: input });

      // Weather detection
      const weatherMatch = input.trim().match(/^weather\s*(in\s*)?(.+)$/i);
      let city = "";
      if (weatherMatch) {
        city = weatherMatch[2].trim();
        endpoint = `/weather?city=${encodeURIComponent(city)}`;
        method = "GET";
        body = null;
      }

      const res = await fetch(`${backendURL}${endpoint}`, {
        method,
        headers: { "Content-Type": "application/json" },
        body,
      });

      if (!res.ok) throw new Error("Network response was not ok");

      const data = await res.json();

      // Add bot message
      setMessages((prev) => [...prev, { sender: "bot", text: data.message }]);

      // Update map safely
      if (data.centers && Array.isArray(data.centers) && data.centers.length > 0 && data.centers[0].lat && data.centers[0].lon) {
        setCenters(data.centers);
      } else {
        setCenters([]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error, please try again later." },
      ]);
      setCenters([]);
    }

    setInput("");
  };

  return (
    <div className="app">
      <div className="chat-window">
        <div className="chat-header">🌐 Disaster Relief Assistant</div>
        <div className="chat-body">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="chat-footer">
          <input
            type="text"
            placeholder="Ask about weather or relief centers..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>

      {Array.isArray(centers) && centers.length > 0 && centers[0].lat && centers[0].lon && (
        <div className="map-container">
          <MapContainer
            center={[centers[0].lat, centers[0].lon]}
            zoom={12}
            style={{ height: "300px", width: "100%" }}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {centers.map((c, idx) =>
              c.lat && c.lon ? (
                <Marker key={idx} position={[c.lat, c.lon]}>
                  <Popup>{c.name}</Popup>
                </Marker>
              ) : null
            )}
          </MapContainer>
        </div>
      )}
    </div>
  );
}

export default App;
