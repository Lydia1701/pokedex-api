import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pokedex.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5/weather")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "1ed8feb9bd413233956426b2b99b3242")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Paris,FR")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "600"))