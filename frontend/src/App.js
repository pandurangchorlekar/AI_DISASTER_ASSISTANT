import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [reliefCenters, setReliefCenters] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      setMessages([...newMessages, { sender: "bot", text: data.message }]);

      // If relief centers present → store them for map
      if (data.relief_centers) {
        setReliefCenters(data.relief_centers);
      } else {
        setReliefCenters([]); // clear old pins
      }

    } catch (error) {
      setMessages([...newMessages, { sender: "bot", text: "⚠️ Server error." }]);
    }

    setInput("");
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>💬 AI Disaster Relief Assistant</h2>
      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.sender === "user" ? "#DCF8C6" : "#FFF",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Map Section */}
      {reliefCenters.length > 0 && (
        <div style={{ height: "300px", marginTop: "10px" }}>
          <MapContainer
            center={[reliefCenters[0].lat, reliefCenters[0].lng]}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {reliefCenters.map((center, idx) => (
              <Marker key={idx} position={[center.lat, center.lng]}>
                <Popup>{center.name}</Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      )}

      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button style={styles.button} onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

const styles = {
  container: { width: "400px", margin: "20px auto", fontFamily: "Arial, sans-serif" },
  header: { textAlign: "center", marginBottom: "10px" },
  chatBox: { border: "1px solid #ccc", padding: "10px", height: "300px", overflowY: "auto", display: "flex", flexDirection: "column" },
  message: { margin: "5px", padding: "10px", borderRadius: "10px", maxWidth: "70%" },
  inputBox: { display: "flex", marginTop: "10px" },
  input: { flex: 1, padding: "10px", borderRadius: "5px", border: "1px solid #ccc" },
  button: { padding: "10px 15px", marginLeft: "5px", background: "#25D366", color: "white", border: "none", borderRadius: "5px" },
};

export default App;
