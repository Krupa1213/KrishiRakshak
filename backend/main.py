from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import farmer, crop, weather_satellite
from backend.routes import disease
from backend.routes import advisory, market, farm_profile

from backend.crop_health.crop_health_api import router as crop_health_router
from backend.decision_support.decision_api import router as decision_support_router


app = FastAPI(
    title="KrishiRakshak API",
    description="AI-powered agricultural decision support system",
    version="1.0.0"
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.109:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Existing routes
app.include_router(farmer.router)
app.include_router(crop.router)
app.include_router(disease.router)
app.include_router(advisory.router)
app.include_router(market.router)
app.include_router(weather_satellite.router)

# Friend's new backend routes
app.include_router(farm_profile.router)
app.include_router(crop_health_router)
app.include_router(decision_support_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to KrishiRakshak API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }