import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [farmId, setFarmId] = useState("");
  const [cropImage, setCropImage] = useState(null);

  const [profile, setProfile] = useState(null);
  const [cropHealth, setCropHealth] = useState(null);
  const [decision, setDecision] = useState(null);
  const [simulation, setSimulation] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // =========================
  // LOAD FARM PROFILE
  // =========================

  async function loadFarmProfile() {
    if (!farmId.trim()) {
      setMessage("Please enter a Farm ID.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `${API_BASE}/farmers/profile/${farmId}`
      );

      if (!response.ok) {
        throw new Error("Unable to load farm profile.");
      }

      const data = await response.json();

      setProfile(data);
      setMessage("Farm profile loaded successfully.");
    } catch (error) {
      console.error(error);
      setMessage(
        "Unable to load farm profile. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  // =========================
  // CROP HEALTH IMAGE
  // =========================

  async function analyzeCropImage() {
    if (!cropImage) {
      setMessage("Please select a crop image first.");
      return;
    }

    setLoading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", cropImage);

    try {
      const response = await fetch(
        `${API_BASE}/crop-health/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Crop image analysis failed.");
      }

      const data = await response.json();

      setCropHealth(data);
      setMessage("Crop image analyzed successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Unable to analyze the crop image.");
    } finally {
      setLoading(false);
    }
  }

  // =========================
  // DECISION SUPPORT
  // =========================

  async function getRecommendations() {
    if (!profile) {
      setMessage("Load a farm profile first.");
      return;
    }

    const overallRisk = profile.overall_risk || "Medium";
    const weatherRisk = profile.weather_risk || "Medium";
    const ndviRisk = profile.ndvi_risk || "Medium";

    try {
      const response = await fetch(
        `${API_BASE}/decision-support/recommendations`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            overall_risk: overallRisk,
            weather_risk: weatherRisk,
            ndvi_risk: ndviRisk,
            crop_health_prediction:
              cropHealth?.prediction || null,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Recommendation request failed.");
      }

      const data = await response.json();

      setDecision(data);
      setMessage("Decision support generated.");
    } catch (error) {
      console.error(error);
      setMessage("Unable to generate recommendations.");
    }
  }

  // =========================
  // WHAT-IF SIMULATOR
  // =========================

  async function runSimulation(action) {
    const score =
      decision?.overall_score ??
      profile?.overall_score ??
      60;

    try {
      const response = await fetch(
        `${API_BASE}/decision-support/what-if`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            overall_score: Number(score),
            action: action,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Simulation failed.");
      }

      const data = await response.json();

      setSimulation(data);
      setMessage("What-If simulation completed.");
    } catch (error) {
      console.error(error);
      setMessage("Unable to run the simulation.");
    }
  }

  return (
    <div className="app">

      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">
        <h2>🌾 KrishiRakshak</h2>

        <p className="tagline">
          Predict. Prevent. Protect.
        </p>

        <nav>
          <button>🏠 Dashboard</button>
          <button>👨‍🌾 Farm Profile</button>
          <button>🌱 Crop Health</button>
          <button>🌦️ Weather & Satellite</button>
          <button>🤖 AI Decision Support</button>
          <button>🔮 What-If Simulator</button>
        </nav>
      </aside>

      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="main-content">

        <header>
          <h1>KrishiRakshak AI 🌾</h1>

          <p>
            AI-assisted farm risk and decision support system
          </p>
        </header>

        {/* =========================
            FARM PROFILE
        ========================= */}

        <section className="dashboard-section">

          <h2>👨‍🌾 Farm Profile</h2>

          <div className="farm-input">

            <input
              type="text"
              placeholder="Enter Farm ID"
              value={farmId}
              onChange={(e) =>
                setFarmId(e.target.value)
              }
            />

            <button onClick={loadFarmProfile}>
              Load Farm
            </button>

          </div>

          {profile && (
            <div className="cards">

              <div className="card">
                <h3>👨‍🌾 Farmer</h3>

                <p className="value">
                  {profile.farm?.farmer_name || "N/A"}
                </p>
              </div>

              <div className="card">
                <h3>🌱 Crop</h3>

                <p className="value">
                  {profile.crop?.crop_name || "N/A"}
                </p>
              </div>

              <div className="card">
                <h3>🌍 Soil</h3>

                <p className="value">
                  {profile.soil?.soil_type || "N/A"}
                </p>
              </div>

              <div className="card">
                <h3>💰 Market</h3>

                <p className="value">
                  {profile.market?.price_per_quintal
                    ? `₹${profile.market.price_per_quintal}`
                    : "N/A"}
                </p>
              </div>

            </div>
          )}

        </section>

        {/* =========================
            CROP HEALTH
        ========================= */}

        <section className="dashboard-section">

          <h2>🌱 Crop Health Analysis</h2>

          <input
            type="file"
            accept="image/*"
            onChange={(e) =>
              setCropImage(e.target.files[0])
            }
          />

          <button
            onClick={analyzeCropImage}
            disabled={loading}
          >
            🔍 Analyze Crop Image
          </button>

          {cropHealth && (
            <div className="result-box">

              <h3>
                Prediction: {cropHealth.prediction}
              </h3>

              <p>
                Confidence:{" "}
                {(cropHealth.confidence * 100).toFixed(0)}%
              </p>

              <p>
                <strong>Recommendation:</strong>{" "}
                {cropHealth.recommendation}
              </p>

            </div>
          )}

        </section>

        {/* =========================
            DECISION SUPPORT
        ========================= */}

        <section className="dashboard-section">

          <h2>🤖 AI Decision Support</h2>

          <button
            onClick={getRecommendations}
            disabled={!profile}
          >
            Generate Recommendations
          </button>

          {decision && (
            <div className="result-box">

              <h3>
                Overall Risk:{" "}
                {decision.overall_risk}
              </h3>

              <ul>
                {decision.recommendations?.map(
                  (recommendation, index) => (
                    <li key={index}>
                      {recommendation}
                    </li>
                  )
                )}
              </ul>

            </div>
          )}

        </section>

        {/* =========================
            WHAT-IF SIMULATOR
        ========================= */}

        <section className="dashboard-section">

          <h2>🔮 What-If Decision Simulator</h2>

          <p>
            Explore how different farm-management
            actions may affect the estimated risk.
          </p>

          <div className="actions">

            <button
              onClick={() =>
                runSimulation("increase irrigation")
              }
            >
              💧 Increase Irrigation
            </button>

            <button
              onClick={() =>
                runSimulation("reduce irrigation")
              }
            >
              🚿 Reduce Irrigation
            </button>

            <button
              onClick={() =>
                runSimulation("improve drainage")
              }
            >
              🌊 Improve Drainage
            </button>

            <button
              onClick={() =>
                runSimulation("apply fertilizer")
              }
            >
              🌱 Apply Fertilizer
            </button>

            <button
              onClick={() =>
                runSimulation("use disease control")
              }
            >
              🦠 Disease Control
            </button>

            <button
              onClick={() =>
                runSimulation("monitor crop closely")
              }
            >
              👀 Monitor Closely
            </button>

          </div>

          {simulation && (
            <div className="result-box">

              <h3>
                What If:{" "}
                {simulation.action}
              </h3>

              <p>
                Original Risk:{" "}
                <strong>
                  {simulation.original_risk}
                </strong>
              </p>

              <p>
                Original Score:{" "}
                {simulation.original_score}
              </p>

              <p>
                Simulated Risk:{" "}
                <strong>
                  {simulation.simulated_risk}
                </strong>
              </p>

              <p>
                Simulated Score:{" "}
                {simulation.simulated_score}
              </p>

              <p>
                📊 {simulation.impact}
              </p>

              <small>
                {simulation.note}
              </small>

            </div>
          )}

        </section>

        {/* =========================
            STATUS
        ========================= */}

        {message && (
          <div className="status-message">
            {message}
          </div>
        )}

      </main>
    </div>
  );
}

export default App;