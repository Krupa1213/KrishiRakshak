
import { useEffect, useState } from "react";
import {
  getFarmers,
  recommendCrop,
  getFarmRisk,
  detectDisease,
  getCropHistory
} from "./services/api";

function App() {
  const [farmer, setFarmer] = useState(null);
  const [cropHistory, setCropHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [recommendedCrop, setRecommendedCrop] = useState("");
  const [farmRisk, setFarmRisk] = useState(null);
  const [farmRiskLoading, setFarmRiskLoading] = useState(false);
  const [farmRiskError, setFarmRiskError] = useState("");
  const [cropData, setCropData] = useState({
  N: "",
  P: "",
  K: "",
  temperature: "",
  humidity: "",
  ph: "",
  rainfall: "",
});
const [diseaseImage, setDiseaseImage] = useState(null);
const [diseaseResult, setDiseaseResult] = useState(null);
const [diseaseLoading, setDiseaseLoading] = useState(false);
const [diseaseError, setDiseaseError] = useState("");

const [cropLoading, setCropLoading] = useState(false);
const [cropError, setCropError] = useState("");
const handleCropRecommendation = async (e) => {
  e.preventDefault();

  setCropLoading(true);
  setCropError("");
  setRecommendedCrop("Analyzing...");

  try {
    const data = await recommendCrop({
      N: Number(cropData.N),
      P: Number(cropData.P),
      K: Number(cropData.K),
      temperature: Number(cropData.temperature),
      humidity: Number(cropData.humidity),
      ph: Number(cropData.ph),
      rainfall: Number(cropData.rainfall),
    });

    setRecommendedCrop(data.recommended_crop);
    const history = await getCropHistory();
setCropHistory(history);
  } catch (error) {
    console.error(error);
    setCropError("Unable to get crop recommendation.");
    setRecommendedCrop("Unavailable");
  } finally {
    setCropLoading(false);
  }
};

const handleCropInputChange = (e) => {
  const { name, value } = e.target;

  setCropData((previous) => ({
    ...previous,
    [name]: value,
  }));
};

const handleDiseaseImageChange = (e) => {
  const file = e.target.files?.[0];

  setDiseaseImage(file || null);
  setDiseaseResult(null);
  setDiseaseError("");
};

const handleDiseaseDetection = async () => {
  if (!diseaseImage) {
    setDiseaseError("Please select a crop image.");
    return;
  }

  setDiseaseLoading(true);
  setDiseaseError("");

  try {
    const result = await detectDisease(diseaseImage);
    setDiseaseResult(result);
  } catch (error) {
    console.error(error);
    setDiseaseError(
      error.message || "Failed to detect crop disease."
    );
  } finally {
    setDiseaseLoading(false);
  }
};

  useEffect(() => {
    // Get farmer information from FastAPI
    getFarmers()
      .then((data) => {
        if (data.length > 0) {
          setFarmer(data[0]);
        }
      })
      .catch((error) => {
        console.error(error);
        setError("Unable to load farmer information.");
      })
      .finally(() => {
        setLoading(false);
      });

    getCropHistory()
    .then((data) => {
      setCropHistory(data);
    })
    .catch((error) => {
      console.error("Failed to load crop history:", error);
    });

  }, []);

  const checkFarmRisk = async () => {
  setFarmRiskLoading(true);
  setFarmRiskError("");

  if (!navigator.geolocation) {
    setFarmRiskError("Location is not supported by this browser.");
    setFarmRiskLoading(false);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      try {
        const { latitude, longitude } = position.coords;

        const data = await getFarmRisk(latitude, longitude);
        setFarmRisk(data);
      } catch (error) {
        console.error(error);
        setFarmRiskError(error.message);
      } finally {
        setFarmRiskLoading(false);
      }
    },
    (error) => {
      console.error(error);
      setFarmRiskError(
        "Unable to get your location. Please allow location access."
      );
      setFarmRiskLoading(false);
    }
  );
};

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>🌾 KrishiRakshak</h2>

        <nav>
          <button onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
  🏠 Dashboard
</button>
          <button onClick={() => document.getElementById("farmer-profile")?.scrollIntoView({ behavior: "smooth" })}>
  👨‍🌾 Farmer Profile
</button>
          <button onClick={() => document.getElementById("crop-recommendation")?.scrollIntoView({ behavior: "smooth" })}>
  🌱 Crop Recommendation
</button>
          <button onClick={() => document.getElementById("disease-detection")?.scrollIntoView({ behavior: "smooth" })}>
  🔬 Disease Detection
</button>
          <button onClick={() => document.getElementById("weather")?.scrollIntoView({ behavior: "smooth" })}>
  🌦️ Weather
</button>
          <button onClick={() => document.getElementById("market-prices")?.scrollIntoView({ behavior: "smooth" })}>
  💰 Market Prices
</button>
          <button onClick={() => document.getElementById("alerts")?.scrollIntoView({ behavior: "smooth" })}>
  🔔 Alerts
</button>

<button onClick={() => document.getElementById("farm-risk")?.scrollIntoView({ behavior: "smooth" })}>
  ⚠️ Farm Risk
</button>

        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header>
          <h1>Good Morning, Farmer 👋</h1>
          <p>Smart decisions for better farming</p>
        </header>

        {/* Dashboard Cards */}
        <section className="cards">
          {/* Weather */}
          <div id="weather" className="card">
  <h3>🌦️ Weather</h3>
            <p className="value">28°C</p>
            <p>Partly Cloudy</p>
          </div>

          {/* Crop Recommendation */}
          <div className="card">
            <h3>🌱 Crop Recommendation</h3>
            <p className="value">{recommendedCrop}</p>
            <p>Recommended by AI model</p>
          </div>

          {/* Market Price */}
          <div id="market-prices" className="card">
  <h3>💰 Market Price</h3>
            <p className="value">₹2,450</p>
            <p>Wheat / Quintal</p>
          </div>

          {/* Alerts */}
          <div id="alerts" className="card">
  <h3>🔔 Alerts</h3>
            <p className="value">2</p>
            <p>Important notifications</p>
          </div>
        </section>

        {/* Crop Recommendation Form */}
<section id="crop-recommendation" className="dashboard-section">
  <h2>🌱 Crop Recommendation</h2>
  <p>Enter your soil and weather conditions to get an AI-based crop recommendation.</p>

  <form onSubmit={handleCropRecommendation} className="crop-form">

    <div className="form-grid">

      <div>
        <label>Nitrogen (N)</label>
        <input
          type="number"
          name="N"
          value={cropData.N}
          onChange={handleCropInputChange}
          placeholder="e.g. 90"
          required
        />
      </div>

      <div>
        <label>Phosphorus (P)</label>
        <input
          type="number"
          name="P"
          value={cropData.P}
          onChange={handleCropInputChange}
          placeholder="e.g. 42"
          required
        />
      </div>

      <div>
        <label>Potassium (K)</label>
        <input
          type="number"
          name="K"
          value={cropData.K}
          onChange={handleCropInputChange}
          placeholder="e.g. 43"
          required
        />
      </div>

      <div>
        <label>Temperature (°C)</label>
        <input
          type="number"
          step="0.1"
          name="temperature"
          value={cropData.temperature}
          onChange={handleCropInputChange}
          placeholder="e.g. 20.8"
          required
        />
      </div>

      <div>
        <label>Humidity (%)</label>
        <input
          type="number"
          step="0.1"
          name="humidity"
          value={cropData.humidity}
          onChange={handleCropInputChange}
          placeholder="e.g. 82"
          required
        />
      </div>

      <div>
        <label>Soil pH</label>
        <input
          type="number"
          step="0.1"
          name="ph"
          value={cropData.ph}
          onChange={handleCropInputChange}
          placeholder="e.g. 6.5"
          required
        />
      </div>

      <div>
        <label>Rainfall (mm)</label>
        <input
          type="number"
          step="0.1"
          name="rainfall"
          value={cropData.rainfall}
          onChange={handleCropInputChange}
          placeholder="e.g. 202.9"
          required
        />
      </div>

    </div>

    <button type="submit" disabled={cropLoading}>
      {cropLoading ? "🔄 Analyzing..." : "🌱 Recommend Crop"}
    </button>

  </form>

  {cropError && (
    <p>{cropError}</p>
  )}

  {recommendedCrop && recommendedCrop !== "Analyzing..." && (
    <div className="farmer-info">
      <h3>🤖 AI Recommendation</h3>
      <p>
        <strong>Recommended Crop:</strong>{" "}
        {recommendedCrop}
      </p>
    </div>
  )}
</section>

{/* Crop Recommendation History */}
<section className="dashboard-section">
  <h2>📋 Crop Recommendation History</h2>

  {cropHistory.length === 0 ? (
    <p>No crop recommendation history available.</p>
  ) : (
    <div className="farmer-info">
      {cropHistory.map((item, index) => (
        <div key={index}>
          <p>
            <strong>Recommendation:</strong>{" "}
            {item.recommended_crop}
          </p>

          <p>
            <strong>N:</strong> {item.input.N} |{" "}
            <strong>P:</strong> {item.input.P} |{" "}
            <strong>K:</strong> {item.input.K}
          </p>

          <p>
            <strong>Temperature:</strong>{" "}
            {item.input.temperature}°C |{" "}
            <strong>Humidity:</strong>{" "}
            {item.input.humidity}%
          </p>

          <p>
            <strong>pH:</strong> {item.input.ph} |{" "}
            <strong>Rainfall:</strong>{" "}
            {item.input.rainfall} mm
          </p>

          <hr />
        </div>
      ))}
    </div>
  )}
</section>

{/* Crop Disease Detection */}
<section id="disease-detection" className="dashboard-section">
  <h2>🔬 Crop Disease Detection</h2>

  <p>
    Upload a crop image and let KrishiRakshak AI identify possible
    crop diseases.
  </p>

  <input
    type="file"
    accept="image/*"
    onChange={handleDiseaseImageChange}
  />

  {diseaseImage && (
    <p>
      <strong>Selected Image:</strong> {diseaseImage.name}
    </p>
  )}

  <button
    onClick={handleDiseaseDetection}
    disabled={diseaseLoading}
  >
    {diseaseLoading
      ? "🔄 Analyzing Image..."
      : "🔬 Detect Crop Disease"}
  </button>

  {diseaseError && (
    <p>{diseaseError}</p>
  )}

  {diseaseResult && (
    <div className="farmer-info">
      <h3>🤖 AI Disease Analysis</h3>

      <p>
        <strong>Prediction:</strong>{" "}
        {diseaseResult.prediction}
      </p>

      <p>
        <strong>Confidence:</strong>{" "}
        {diseaseResult.confidence}%
      </p>
    </div>
  )}
</section>

                {/* Farm Risk Analysis */}
        <section id="farm-risk" className="dashboard-section">
          <h2>⚠️ Farm Risk Analysis</h2>

          <button onClick={checkFarmRisk}>
            🛰️ Check Farm Risk
          </button>

          {farmRiskLoading && (
            <p>Analyzing weather and satellite data...</p>
          )}

          {farmRiskError && (
            <p>Farm risk unavailable: {farmRiskError}</p>
          )}

          {farmRisk && (
            <div className="farmer-info">
              <p>
                <strong>Weather Risk:</strong>{" "}
                {farmRisk.weather.risk.overall_risk}
              </p>

              <p>
                <strong>NDVI Risk:</strong>{" "}
                {farmRisk.satellite.risk_level}
              </p>

              <p>
                <strong>Vegetation Condition:</strong>{" "}
                {farmRisk.satellite.vegetation_condition}
              </p>

              <p>
                <strong>Overall Farm Risk:</strong>{" "}
                {farmRisk.farm_risk.overall_risk}
              </p>

              <p>
                <strong>Risk Score:</strong>{" "}
                {farmRisk.farm_risk.overall_score} / 100
              </p>
            </div>
          )}
        </section>

        {/* Farmer Information */}
        <section id="farmer-profile" className="dashboard-section">
  <h2>👨‍🌾 Farmer Information</h2>

          {loading && (
            <p>Loading farmer information...</p>
          )}

          {error && (
            <p>{error}</p>
          )}

          {!loading && !error && farmer && (
            <div className="farmer-info">
              <p>
                <strong>Name:</strong> {farmer.name}
              </p>

              <p>
                <strong>Location:</strong>{" "}
                {farmer.district}, {farmer.state}
              </p>

              <p>
                <strong>Land Size:</strong>{" "}
                {farmer.land_size} acres
              </p>

              <p>
                <strong>Crops:</strong>{" "}
                {farmer.crops.join(", ")}
              </p>
            </div>
          )}

          {!loading && !error && !farmer && (
            <p>No farmer information found.</p>
          )}
        </section>

        {/* Quick Actions */}
        <section className="dashboard-section">
          <h2>Quick Actions</h2>

          <div className="actions">
            <button onClick={() => document.getElementById("crop-recommendation")?.scrollIntoView({ behavior: "smooth" })}>
              🌱 Get Crop Recommendation
            </button>

           <button onClick={() => document.getElementById("weather")?.scrollIntoView({ behavior: "smooth" })}>
  🌦️ Check Weather
</button>

            <button onClick={() => document.getElementById("market-prices")?.scrollIntoView({ behavior: "smooth" })}>
  💰 Check Market Prices
</button>

            <button onClick={() => document.getElementById("farm-risk")?.scrollIntoView({ behavior: "smooth" })}>
  ⚠️ Check Farm Risk
</button>

            <button onClick={() => document.getElementById("disease-detection")?.scrollIntoView({ behavior: "smooth" })}>
  🔬 Check Crop Disease
</button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

