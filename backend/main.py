from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import weather_satellite, farmer, farm_profile
from backend.crop_health.crop_health_api import router as crop_health_router


app = FastAPI(
    title="KrishiRakshak API",
    description="AI-powered agricultural decision support system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(weather_satellite.router)
app.include_router(farmer.router)
app.include_router(farm_profile.router)
app.include_router(crop_health_router)


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