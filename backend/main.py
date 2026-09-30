from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import PROJECT_NAME, ENVIRONMENT, DEBUG
from backend.schemas.api_schemas import HealthResponse
from backend.api.machine import router as machine_router


app = FastAPI(
    title=PROJECT_NAME,
    description="AI-powered industrial intelligence and predictive maintenance backend.",
    version="1.0.0",
    debug=DEBUG
)


# Allow React frontend to communicate with FastAPI
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


# Register machine API
app.include_router(machine_router)


@app.get("/", response_model=HealthResponse)
def root():
    return {
        "status": "running",
        "project": PROJECT_NAME,
        "environment": ENVIRONMENT
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "healthy",
        "project": PROJECT_NAME,
        "environment": ENVIRONMENT
    }


@app.get("/dashboard/summary")
def dashboard_summary():
    """
    Dashboard summary endpoint.

    Current values represent the project's configured
    demonstration machine fleet. They will later be
    replaced by dynamically calculated values from
    the machine/AI data pipeline.
    """

    return {
        "total_machines": 12,
        "healthy": 9,
        "warning": 2,
        "critical": 1,
        "system_status": "Online"
    }