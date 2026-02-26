import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# API Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

# CORS Configuration
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "['http://localhost:3000', 'http://localhost:3001']")

# Application Title and Description
APP_TITLE = "With You API"
APP_DESCRIPTION = "Identity-First AI Architecture - When memory fades, presence remains. API for cognitive mesh agents: Aurora, Harbor, Roots, Solace, Legacy, Echo, and Guardian."
APP_VERSION = "2.0.0"

# GitHub Models / Copilot Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MODEL_ENDPOINT = os.getenv("MODEL_ENDPOINT", "https://models.github.ai/inference/")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
