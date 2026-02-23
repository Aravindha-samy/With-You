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
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "['http://localhost:3000', 'http://localhost:3001']")

# Application Title and Description
APP_TITLE = "WithYou API"
APP_DESCRIPTION = "API for WithYou - Patient Care and Memory Management System"
APP_VERSION = "1.0.0"
