from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Pokemon
from .schemas import PokemonCreate, PokemonUpdate

def create_pokemon(db: Session, data: PokemonCreate) -> Pokemon:
    p = Pokemon(name=data.name, type=data.type.lower(), power=data.power)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_pokemon(db: Session, pokemon_id: int) -> Pokemon | None:
    return db.get(Pokemon, pokemon_id)

def get_pokemon_by_name(db: Session, name: str) -> Pokemon | None:
    stmt = select(Pokemon).where(Pokemon.name == name)
    return db.scalar(stmt)

def list_pokemons(db: Session, skip: int = 0, limit: int = 50) -> list[Pokemon]:
    stmt = select(Pokemon).offset(skip).limit(limit)
    return list(db.scalars(stmt))

def update_pokemon(db: Session, pokemon_id: int, data: PokemonUpdate) -> Pokemon | None:
    p = db.get(Pokemon, pokemon_id)
    if not p:
        return None
    if data.name is not None: p.name = data.name
    if data.type is not None: p.type = data.type.lower()
    if data.power is not None: p.power = data.power
    db.commit()
    db.refresh(p)
    return p

def delete_pokemon(db: Session, pokemon_id: int) -> bool:
    p = db.get(Pokemon, pokemon_id)
    if not p: return False
    db.delete(p)
    db.commit()
    return True
