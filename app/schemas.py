from pydantic import BaseModel, Field

class PokemonBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    type: str
    power: int = Field(..., ge=0)

class PokemonCreate(PokemonBase):
    pass

class PokemonUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    power: int | None = Field(None, ge=0)

class PokemonOut(PokemonBase):
    id: int
    power_current: int

    class Config:
        from_attributes = True
