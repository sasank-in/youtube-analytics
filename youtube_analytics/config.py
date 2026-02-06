"""Configuration Module

Loads environment variables and configuration settings
from .env file using python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Database Configuration
# Using SQLite for simplicity - can be changed to PostgreSQL
DB_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///youtube_analytics.db"
)

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
