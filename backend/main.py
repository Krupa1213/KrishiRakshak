from fastapi import FastAPI

app = FastAPI(
    title="KrishiRakshak API",
    description="AI-powered agricultural decision support system",
    version="1.0.0"
)


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
