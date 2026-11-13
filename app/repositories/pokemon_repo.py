import json
from pathlib import Path
from app.models.pokemon import Pokemon

# Calculamos la ruta relativa al archivo JSON dentro de app/data/
RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-ugly.json"


def _cargar_json() -> list[dict]:
    with RUTA_DATOS.open("r", encoding="utf-8") as file:
        return json.load(file)


def obtener_todos_pokemons() -> list[Pokemon]:
    datos_raw = _cargar_json()
    pokemons = []
    
    for item in datos_raw:
        pokemon = Pokemon(
            id=item["id"],
            name=item["name"],
            height=item["height"],
            weight=item["weight"],
            types=item["types"],
            stats=item.get("stats", []),
            moves=item.get("moves", item.get("attacks", [])),
            sprites=item.get("sprites", {})
        )
        pokemons.append(pokemon)
        
    return pokemons


def buscar_por_id(pokemon_id: int) -> Pokemon | None:
    for pokemon in obtener_todos_pokemons():
        if pokemon.id == pokemon_id:
            return pokemon
    return None


def buscar_por_nombre(nombre: str) -> Pokemon | None:
    nombre_normalizado = nombre.strip().lower()
    for pokemon in obtener_todos_pokemons():
        if pokemon.name.lower() == nombre_normalizado:
            return pokemon
    return None