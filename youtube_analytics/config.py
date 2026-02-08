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
# IMPORTANT: Set DATABASE_URL in .env for PostgreSQL
# Format: postgresql://username:password@localhost:5432/youtube_db
# If not set, defaults to SQLite with ABSOLUTE path
db_url_env = os.getenv("DATABASE_URL", None)

if db_url_env:
    DB_URL = db_url_env
else:
    # Use absolute path for SQLite to avoid path confusion
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_FILE = os.path.join(PROJECT_ROOT, "youtube_analytics.db")
    DB_URL = f"sqlite:///{DB_FILE}"
    print(f"📂 Using SQLite database at: {DB_FILE}")

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Analytics Settings
TOP_VIDEOS_LIMIT = int(os.getenv("TOP_VIDEOS_LIMIT", "50"))

# Database Debug Mode
DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"  # Logs SQL queries if True
