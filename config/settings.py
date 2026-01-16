import os
from dotenv import load_dotenv

load_dotenv()

# API
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL")

# DB
DATABASE_URL = os.getenv("DATABASE_URL")
MODELS_MODULES = ["src.db"]
