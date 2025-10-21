import json
import httpx
from redis import asyncio as aioredis
from .config import WEATHER_API_URL, WEATHER_API_KEY, DEFAULT_CITY, CACHE_TTL_SECONDS

def _cache_key(city: str) -> str:
    return f"weather:{city}"

async def get_weather(redis: aioredis.Redis, city: str = DEFAULT_CITY) -> dict:
    key = _cache_key(city)
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)

    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric", "lang": "fr"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(WEATHER_API_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    await redis.set(key, json.dumps(data), ex=CACHE_TTL_SECONDS)
    return data

def is_raining(weather_json: dict) -> bool:
    """Renvoie True si la météo indique Rain ou Drizzle."""
    weather_list = weather_json.get("weather", [])
    mains = [w.get("main", "").lower() for w in weather_list]
    return any(m in ("rain", "drizzle") for m in mains)

def get_temp_c(weather_json: dict) -> float | None:
    return weather_json.get("main", {}).get("temp")

def is_cold(weather_json: dict, threshold: float = 5.0) -> bool:
    t = get_temp_c(weather_json)
    return t is not None and t < threshold
