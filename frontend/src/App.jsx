import { useEffect, useState } from "react";

import {
  getFarmers,
  getFarmProfile,
  analyzeCropImage,
  getRecommendations,
  simulateWhatIf,
} from "./services/api";

import "./App.css";


function App() {
  // =========================
  // FARM DATA
  // =========================

  const [farmId, setFarmId] = useState("FARM001");
  const [farmer, setFarmer] = useState(null);
  const [profile, setProfile] = useState(null);

  // =========================
  // UI STATES
  // =========================

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // =========================
  // CROP HEALTH
  // =========================

  const [selectedImage, setSelectedImage] = useState(null);
  const [cropHealth, setCropHealth] = useState(null);
  const [imageLoading, setImageLoading] = useState(false);

  // =========================
  // DECISION SUPPORT
  // =========================

  const [decisionSupport, setDecisionSupport] = useState(null);
  const [recommendationLoading, setRecommendationLoading] = useState(false);

  // =========================
  // WHAT-IF
  // =========================

  const [simulation, setSimulation] = useState(null);
  const [simulationLoading, setSimulationLoading] = useState(false);


  // =========================
  // LOAD FARMERS
  // =========================

  useEffect(() => {
    loadFarmers();
  }, []);


  async function loadFarmers() {
    try {
      setLoading(true);
      setError("");

      const data = await getFarmers();

      if (data.length > 0) {
        setFarmer(data[0]);
      }
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the backend.");
    } finally {
      setLoading(false);
    }
  }


  // =========================
  // LOAD FARM PROFILE
  // =========================

  async function handleLoadProfile() {
    try {
      setLoading(true);
      setError("");
      setMessage("");

      const data = await getFarmProfile(farmId);

      setProfile(data);

      if (!data.farm) {
        setMessage("No farm found for this Farm ID.");
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  // =========================
  // CROP IMAGE
  // =========================

  function handleImageChange(event) {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setSelectedImage(file);
    setCropHealth(null);
    setError("");
    setMessage("");
  }


  async function handleCropAnalysis() {
    if (!selectedImage) {
      setError("Please select a crop image first.");
      return;
    }

    try {
      setImageLoading(true);
      setError("");
      setMessage("");

      const result = await analyzeCropImage(selectedImage);

      setCropHealth(result);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setImageLoading(false);
    }
  }


  // =========================
  // RECOMMENDATIONS
  // =========================

  async function handleRecommendations() {
    try {
      setRecommendationLoading(true);
      setError("");
      setMessage("");

      /*
       * Temporary risk values are used here because
       * the current farm profile API does not yet return
       * the combined weather + satellite risk score.
       *
       * We will connect the real risk calculation next.
       */

      const data = {
        overall_risk: "Medium",
        weather_risk: "Medium",
        ndvi_risk: "Medium",
        crop_health_prediction:
          cropHealth?.prediction || null,
      };

      const result = await getRecommendations(data);

      setDecisionSupport(result);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setRecommendationLoading(false);
    }
  }


  // =========================
  // WHAT-IF SIMULATION
  // =========================

  async function handleWhatIf(action) {
    try {
      setSimulationLoading(true);
      setError("");
      setMessage("");

      /*
       * Use the current risk score if available.
       * Until the real farm risk score is connected,
       * 60 is used as the prototype Medium-risk score.
       */

      const currentScore =
        profile?.overall_score ?? 60;

      const result = await simulateWhatIf({
        overall_score: currentScore,
        action: action,
      });

      setSimulation(result);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setSimulationLoading(false);
    }
  }


  return (
    <div className="app">

      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">

        <h2>🌾 KrishiRakshak</h2>

        <p className="sidebar-subtitle">
          Smart Farm Decision Support
        </p>

        <nav>

          <button>
            🏠 Dashboard
          </button>

          <button>
            👨‍🌾 Farm Profile
          </button>

          <button>
            🌱 Crop Health
          </button>

          <button>
            🌦️ Weather
          </button>

          <button>
            🛰️ Satellite
          </button>

          <button>
            🤖 AI Decisions
          </button>

          <button>
            🔮 What-If Simulator
          </button>

        </nav>

      </aside>


      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="main-content">

        <header className="dashboard-header">

          <div>
            <h1>
              KrishiRakshak AI 🌾
            </h1>

            <p>
              Predict. Prevent. Protect the Farmer's Income.
            </p>
          </div>

        </header>


        {/* =========================
            FARM ID
        ========================= */}

        <section className="dashboard-section">

          <h2>👨‍🌾 Select Farm</h2>

          <div className="farm-selector">

            <input
              type="text"
              value={farmId}
              onChange={(event) =>
                setFarmId(event.target.value)
              }
              placeholder="Enter Farm ID"
            />

            <button
              onClick={handleLoadProfile}
              disabled={loading}
            >
              {loading
                ? "Loading..."
                : "Load Farm"}
            </button>

          </div>

          {message && (
            <p className="success-message">
              {message}
            </p>
          )}

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

        </section>


        {/* =========================
            FARM PROFILE
        ========================= */}

        {profile?.farm && (

          <section className="dashboard-section">

            <h2>🌱 Farm Profile</h2>

            <div className="info-grid">

              <div>
                <strong>Farm ID</strong>
                <p>
                  {profile.farm.farm_id}
                </p>
              </div>

              <div>
                <strong>Farmer</strong>
                <p>
                  {profile.farm.farmer_name}
                </p>
              </div>

              <div>
                <strong>Crop</strong>
                <p>
                  {profile.farm.crop}
                </p>
              </div>

              <div>
                <strong>Area</strong>
                <p>
                  {profile.farm.area_acres} acres
                </p>
              </div>

              <div>
                <strong>Soil</strong>
                <p>
                  {profile.soil?.soil_type || "Not available"}
                </p>
              </div>

              <div>
                <strong>Market Price</strong>
                <p>
                  {profile.market?.price_per_quintal
                    ? `₹${profile.market.price_per_quintal}`
                    : "Not available"}
                </p>
              </div>

            </div>

          </section>

        )}


        {/* =========================
            CROP HEALTH
        ========================= */}

        <section className="dashboard-section">

          <h2>🌱 Crop Health Analysis</h2>

          <p>
            Upload a crop image for AI-assisted
            crop-health analysis.
          </p>

          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />

          <br />
          <br />

          <button
            onClick={handleCropAnalysis}
            disabled={
              !selectedImage ||
              imageLoading
            }
          >
            {imageLoading
              ? "Analyzing..."
              : "Analyze Crop Image"}
          </button>


          {cropHealth?.status === "success" && (

            <div className="result-box">

              <h3>
                Crop Health Result
              </h3>

              <p>
                <strong>Prediction:</strong>{" "}
                {cropHealth.prediction}
              </p>

              <p>
                <strong>Confidence:</strong>{" "}
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
            AI RECOMMENDATIONS
        ========================= */}

        <section className="dashboard-section">

          <h2>🤖 AI Decision Support</h2>

          <p>
            Generate farm-management recommendations
            using the available risk indicators.
          </p>

          <button
            onClick={handleRecommendations}
            disabled={recommendationLoading}
          >
            {recommendationLoading
              ? "Generating..."
              : "Generate Recommendations"}
          </button>


          {decisionSupport && (

            <div className="result-box">

              <h3>
                Recommended Actions
              </h3>

              <ul>

                {decisionSupport.recommendations?.map(
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
            Compare hypothetical farm-management
            actions and see how the estimated risk score
            could change.
          </p>


          <div className="actions">

            <button
              onClick={() =>
                handleWhatIf("increase irrigation")
              }
            >
              💧 Increase Irrigation
            </button>

            <button
              onClick={() =>
                handleWhatIf("reduce irrigation")
              }
            >
              💧 Reduce Irrigation
            </button>

            <button
              onClick={() =>
                handleWhatIf("apply fertilizer")
              }
            >
              🌱 Apply Fertilizer
            </button>

            <button
              onClick={() =>
                handleWhatIf("improve drainage")
              }
            >
              💦 Improve Drainage
            </button>

            <button
              onClick={() =>
                handleWhatIf("use disease control")
              }
            >
              🦠 Disease Control
            </button>

            <button
              onClick={() =>
                handleWhatIf("monitor crop closely")
              }
            >
              🔍 Monitor Closely
            </button>

          </div>


          {simulationLoading && (
            <p>
              Running simulation...
            </p>
          )}


          {simulation && (

            <div className="result-box">

              <h3>
                Simulation Result
              </h3>

              <p>
                <strong>Action:</strong>{" "}
                {simulation.action}
              </p>

              <p>
                <strong>Original Risk:</strong>{" "}
                {simulation.original_risk}
              </p>

              <p>
                <strong>Original Score:</strong>{" "}
                {simulation.original_score}
              </p>

              <p>
                <strong>Simulated Risk:</strong>{" "}
                {simulation.simulated_risk}
              </p>

              <p>
                <strong>Simulated Score:</strong>{" "}
                {simulation.simulated_score}
              </p>

              <p>
                <strong>Impact:</strong>{" "}
                {simulation.impact}
              </p>

              <small>
                {simulation.note}
              </small>

            </div>

          )}

        </section>


        {/* =========================
            FARMER INFORMATION
        ========================= */}

        {farmer && (

          <section className="dashboard-section">

            <h2>👨‍🌾 Farmer Information</h2>

            <p>
              <strong>Name:</strong>{" "}
              {farmer.name}
            </p>

            <p>
              <strong>Location:</strong>{" "}
              {farmer.district},{" "}
              {farmer.state}
            </p>

            <p>
              <strong>Land Size:</strong>{" "}
              {farmer.land_size} acres
            </p>

            <p>
              <strong>Crops:</strong>{" "}
              {farmer.crops?.join(", ")}
            </p>

          </section>

        )}

      </main>

    </div>
  );
}


export default App;
