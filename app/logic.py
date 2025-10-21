
from .weather import is_raining, is_cold

def adjusted_power(pokemon_type: str, base_power: int, weather_json: dict) -> int:
    """
    Calcule la puissance ajustée d’un Pokémon selon la météo.
    - Feu perd de la puissance sous la pluie ou par temps froid
    - Eau gagne sous la pluie
    - Glace gagne par temps froid
    """
    power = base_power
    ptype = pokemon_type.lower()

    if is_raining(weather_json):
        if ptype == "water":
            power = round(base_power * 1.2)
        elif ptype == "fire":
            power = round(base_power * 0.8)
    elif is_cold(weather_json):
        if ptype == "ice":
            power = round(base_power * 1.15)
        elif ptype == "fire":
            power = round(base_power * 0.85)

    return max(1, int(power))