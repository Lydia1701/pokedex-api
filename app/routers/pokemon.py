# app/routers/pokemon.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from redis import asyncio as aioredis
import logging

from .. import crud
from ..schemas import PokemonCreate, PokemonUpdate, PokemonOut
from ..dependencies import get_db, get_redis
from ..weather import get_weather
from ..logic import adjusted_power
from ..config import DEFAULT_CITY, WEATHER_API_URL, WEATHER_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pokemons", tags=["pokemons"])

async def _safe_weather_json(redis: aioredis.Redis, city: str | None):
    """Tolérant si Redis / API météo KO : retourne un dict météo minimal."""
    try:
        logger.info(f"  Récupération météo pour: {city or DEFAULT_CITY}")
        logger.info(f" API URL: {WEATHER_API_URL}")
        logger.info(
            f"🔑 API KEY: {WEATHER_API_KEY[:10]}..." if WEATHER_API_KEY else "🔑 API KEY: None"
        )

        weather_data = await get_weather(redis, city or DEFAULT_CITY)
        
        logger.info(f" WEATHER DATA COMPLETE: {weather_data}")
        weather_list = weather_data.get("weather", [])
        logger.info(f" WEATHER LIST: {weather_list}")
        
        temp = weather_data.get("main", {}).get("temp")
        logger.info(f" Météo reçue: temp={temp}°C")
        return weather_data

    except Exception as e:
        logger.error(f" ERREUR météo: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {"weather": [{"main": "Clear"}], "main": {"temp": 20.0}}