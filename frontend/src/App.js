import React, { useState } from "react";
import "./App.css";

function App() {
  const [truckId, setTruckId] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  const handleCheckIn = async (e) => {
    e.preventDefault();

    if (!truckId.trim()) {
      setStatusMessage("❌ Please enter a valid Truck ID.");
      return;
    }

    // Process and clean the Truck ID format right on the screen
    let cleanedId = truckId.toUpperCase().replace(/\s+/g, "");
    if (cleanedId.startsWith("PI") && !cleanedId.includes("-")) {
      const num = cleanedId.replace("PI", "");
      const paddedNum = num.padStart(2, "0");
      cleanedId = `PI-${paddedNum}`;
    }

    setStatusMessage(`⏳ Connecting to port gateway...`);

    try {
      // 🚀 Shoot the data directly to your FastAPI backend server!
      const response = await fetch("http://127.0.0.1:8000/api/checkin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          truck_id: cleanedId,
          driver_phone: "", // Explicitly sending an empty string instead of null
        }),
      });

      const data = await response.json();
      console.log("Backend Response Data:", data);

      if (data.status === "success") {
        setStatusMessage(
          `✅ ${data.message} You are at position #${data.queue_position} in line.`,
        );
      } else if (data.status === "exists") {
        // 💡 Added the 's' here to perfectly match the backend!
        setStatusMessage(
          `ℹ️ ${data.message} Your queue position is #${data.queue_position}.`,
        );
      } else {
        setStatusMessage(
          `❌ Registration error: ${data.message || "Unknown server error"}`,
        );
      }
    } catch (error) {
      console.error("Error connecting to backend:", error);
      setStatusMessage(
        "❌ Network error: Could not reach the backend gateway.",
      );
    }
  };

  return (
    <div className="mobile-container">
      {/* App Header */}
      <header className="app-header">
        <div className="logo-badge">SAGT / PORT</div>
        <h1>Port Flow</h1>
        <p>Internal Logistics Queue</p>
      </header>

      {/* Main Form Card */}
      <main className="card">
        <h3>🚛 Driver Check-In</h3>
        <p className="instruction">
          Enter your vehicle number to enter the virtual customs queue.
        </p>

        <form onSubmit={handleCheckIn}>
          <div className="input-group">
            <label htmlFor="truck-id">Truck ID</label>
            <input
              id="truck-id"
              type="text"
              placeholder="e.g., PI-09"
              value={truckId}
              onChange={(e) => setTruckId(e.target.value)}
            />
          </div>

          <button type="submit" className="btn-primary">
            Join Virtual Queue
          </button>
        </form>

        {statusMessage && <div className="status-box">{statusMessage}</div>}
      </main>

      {/* Footer / Status Indicator */}
      <footer className="app-footer">
        <span className="dot-online"></span> Connected to local gateway
      </footer>
    </div>
  );
}

export default App;
