import { useEffect, useState } from "react";
import { getFarmers } from "./services/api";

function App() {
  const [farmer, setFarmer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
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
  }, []);

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>🌾 KrishiRakshak</h2>

        <nav>
          <button>🏠 Dashboard</button>
          <button>👨‍🌾 Farmer Profile</button>
          <button>🌱 Crop Recommendation</button>
          <button>🌦️ Weather</button>
          <button>💰 Market Prices</button>
          <button>🔔 Alerts</button>
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
          <div className="card">
            <h3>🌦️ Weather</h3>
            <p className="value">28°C</p>
            <p>Partly Cloudy</p>
          </div>

          {/* Crop Recommendation */}
          <div className="card">
            <h3>🌱 Crop Recommendation</h3>
            <p className="value">Wheat</p>
            <p>Suitable for your land</p>
          </div>

          {/* Market Price */}
          <div className="card">
            <h3>💰 Market Price</h3>
            <p className="value">₹2,450</p>
            <p>Wheat / Quintal</p>
          </div>

          {/* Alerts */}
          <div className="card">
            <h3>🔔 Alerts</h3>
            <p className="value">2</p>
            <p>Important notifications</p>
          </div>

        </section>

        {/* Farmer Information */}
        <section className="dashboard-section">
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

            <button>
              🌱 Get Crop Recommendation
            </button>

            <button>
              🌦️ Check Weather
            </button>

            <button>
              💰 Check Market Prices
            </button>

          </div>
        </section>

      </main>
    </div>
  );
}

export default App;