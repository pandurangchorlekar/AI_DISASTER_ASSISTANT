import React, { useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello 👋 I’m your Disaster Relief Assistant." }
  ]);
  const [input, setInput] = useState("");

  const reliefCenters = {
    mangalore: [12.9141, 74.8560],
    mumbai: [19.0760, 72.8777],
    delhi: [28.7041, 77.1025],
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("https://your-backend.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();

      const botMessage = { sender: "bot", text: data.message };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const botMessage = { sender: "bot", text: "⚠️ Server not responding." };
      setMessages((prev) => [...prev, botMessage]);
    }

    setInput("");
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">🌍 AI Disaster Relief Assistant</h2>

      {/* Chat UI */}
      <div className="card p-3 mb-4" style={{ height: "400px", overflowY: "auto" }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`d-flex mb-2 ${msg.sender === "user" ? "justify-content-end" : "justify-content-start"}`}
          >
            <div
              className={`p-2 rounded ${msg.sender === "user" ? "bg-primary text-white" : "bg-light"}`}
              style={{ maxWidth: "75%" }}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="d-flex">
        <input
          className="form-control"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="btn btn-success ms-2" onClick={sendMessage}>
          Send
        </button>
      </div>

      {/* Map */}
      <div className="mt-4">
        <h4>🗺️ Relief Centers</h4>
        <MapContainer center={[12.9141, 74.8560]} zoom={5} style={{ height: "300px", width: "100%" }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors"
          />
          {Object.entries(reliefCenters).map(([city, coords], idx) => (
            <Marker key={idx} position={coords}>
              <Popup>{city.charAt(0).toUpperCase() + city.slice(1)} Relief Center</Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default App;
