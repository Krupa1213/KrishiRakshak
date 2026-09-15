from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import weather_satellite
from backend.routes import farmer


app = FastAPI(
    title="KrishiRakshak API",
    description="AI-powered agricultural decision support system",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(weather_satellite.router)
app.include_router(farmer.router)


@app.get("/")
def home():
    return {
        "message": "KrishiRakshak API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
