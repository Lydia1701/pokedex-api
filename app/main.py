import uvicorn
import logging
from fastapi import FastAPI, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from redis import asyncio as aioredis

from app.db import init_db, get_db
from app import crud
from app.schemas import PokemonCreate, PokemonUpdate, PokemonOut
from app.dependencies import get_redis
from app.weather import get_weather, is_raining, is_cold
from app.logic import adjusted_power
from app.config import DEFAULT_CITY



from fastapi import FastAPI
from .db import init_db  # 👈 on importe l’initialisation
from .routers import pokemon  # 👈 on importe ton routeur

# Création de l’app FastAPI
app = FastAPI(title="Pokedex API", version="1.0.0")

# 🧱 Création des tables au démarrage
@app.on_event("startup")
def on_startup():
    init_db()

# 🚀 Inclusion du routeur Pokémon
app.include_router(pokemon.router)

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur la Pokedex API 🧠",
        "docs": "/docs",
        "pokemons_endpoint": "/pokemons/"
    }


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pokedex + Weather API",
    version="1.0.0",
    description="API de gestion de Pokémon avec effets météo 🌦️",
)

init_db()

async def _safe_weather(redis: aioredis.Redis, city: str | None):
    """Récupère la météo (tolérant aux erreurs API/Redis)."""
    try:
        w = await get_weather(redis, city or DEFAULT_CITY)
        raining, cold = is_raining(w), is_cold(w)
        temp = w.get("main", {}).get("temp")
        logger.info(f"✅ Météo reçue: {city or DEFAULT_CITY} -> {temp}°C, raining={raining}, cold={cold}")
        return raining, cold
    except Exception as e:
        logger.error(f"⚠️ Erreur météo: {type(e).__name__}: {e}")
        return False, False

@app.post("/pokemons/", response_model=PokemonOut, status_code=201, tags=["pokemons"])
async def create_pokemon(
    data: PokemonCreate,
    db: Session = Depends(get_db),
):
    p = crud.create_pokemon(db, data)
    return {
        "id": p.id,
        "name": p.name,
        "type": p.type,
        "power": p.power,
        "power_current": p.power,  # pas d’ajustement météo ici
    }

@app.get("/pokemons/{pokemon_id}", response_model=PokemonOut, tags=["pokemons"])
async def get_pokemon(
    pokemon_id: int,
    city: str | None = Query(None, description="Ville pour météo"),
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    p = crud.get_pokemon(db, pokemon_id)
    if not p:
        raise HTTPException(404, "Pokemon not found")
    raining, cold = await _safe_weather(redis, city)
    return {
        "id": p.id,
        "name": p.name,
        "type": p.type,
        "power": p.power,
        "power_current": adjusted_power(p.type, p.power, raining, cold),
    }

@app.get("/pokemons/", response_model=list[PokemonOut], tags=["pokemons"])
async def list_pokemons(
    skip: int = 0,
    limit: int = Query(50, le=200),
    city: str | None = Query(None, description="Ville pour météo"),
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    pokes = crud.list_pokemons(db, skip, limit)
    raining, cold = await _safe_weather(redis, city)
    return [
        {
            "id": p.id,
            "name": p.name,
            "type": p.type,
            "power": p.power,
            "power_current": adjusted_power(p.type, p.power, raining, cold),
        }
        for p in pokes
    ]

@app.patch("/pokemons/{pokemon_id}", response_model=PokemonOut, tags=["pokemons"])
async def update_pokemon(
    pokemon_id: int,
    data: PokemonUpdate,
    city: str | None = Query(None, description="Ville pour météo"),
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    p = crud.update_pokemon(db, pokemon_id, data)
    if not p:
        raise HTTPException(404, "Pokemon not found")
    raining, cold = await _safe_weather(redis, city)
    return {
        "id": p.id,
        "name": p.name,
        "type": p.type,
        "power": p.power,
        "power_current": adjusted_power(p.type, p.power, raining, cold),
    }

@app.delete("/pokemons/{pokemon_id}", status_code=204, tags=["pokemons"])
async def delete_pokemon(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_pokemon(db, pokemon_id)
    if not deleted:
        raise HTTPException(404, "Pokemon not found")
    return None

@app.get("/", tags=["system"])
async def root():
    return {
        "message": "Bienvenue sur la Pokedex + Weather API 🧠",
        "routes_disponibles": {
            "POST": "/pokemons/",
            "GET": "/pokemons/",
            "GET_ONE": "/pokemons/{pokemon_id}",
            "PATCH": "/pokemons/{pokemon_id}",
            "DELETE": "/pokemons/{pokemon_id}",
        },
        "docs": "/docs",
    }



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
