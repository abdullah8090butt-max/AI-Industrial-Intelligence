import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv(
    "PROJECT_NAME",
    "AI Industrial Intelligence & Predictive Maintenance System"
)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))