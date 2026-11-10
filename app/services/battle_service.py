import random
from app.models.pokemon import Pokemon
from app.repositories.pokemon_repo import obtener_todos_pokemons, buscar_por_nombre


def preparar_combate(pokemon_nombre: str) -> dict | None:
    user_pok = buscar_por_nombre(pokemon_nombre)
    if not user_pok:
        return None

    todos = obtener_todos_pokemons()
    rivales = [p for p in todos if p.name.lower() != user_pok.name.lower()]
    rival_pok = random.choice(rivales) if rivales else user_pok

    movimientos = user_pok.moves
    if len(movimientos) >= 4:
        ataques = random.sample(movimientos, 4)
    else:
        ataques = movimientos

    return {
        "user_pok": user_pok.to_dict(),
        "rival_pok": rival_pok.to_dict(),
        "ataques": ataques
    }