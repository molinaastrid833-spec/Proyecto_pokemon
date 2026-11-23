import random
from app.models.battle import Battle
from app.repositories.pokemon_repo import obtener_todos_pokemons, buscar_por_nombre


def existe_pokemon_para_batalla(nombre: str) -> bool:
    return buscar_por_nombre(nombre) is not None


def iniciar_batalla(trainer: str, pokemon_nombre: str) -> dict | None:
    user_pok = buscar_por_nombre(pokemon_nombre)
    if not user_pok:
        return None

    todos = obtener_todos_pokemons()
    rivales = [p for p in todos if p.name.lower() != user_pok.name.lower()]
    rival_pok = random.choice(rivales) if rivales else user_pok

    battle = Battle.create(
        user_trainer=trainer,
        user_pokemon=user_pok,
        rival_pokemon=rival_pok,
    )
    return battle.to_dict()


def ejecutar_turno(battle_data: dict, move_name: str) -> dict:
    battle = Battle.from_dict(battle_data)
    battle.attack(move_name)
    return battle.to_dict()


def obtener_resumen_batalla(battle_data: dict) -> dict:
    battle = Battle.from_dict(battle_data)
    user_pok = battle.participants[0]["pokemon"]
    rival_pok = battle.participants[1]["pokemon"]

    winner_trainer = None
    winner_pokemon = None
    if battle.winner is not None:
        winner_trainer = battle.participants[battle.winner]["trainer"]
        winner_pokemon = battle.participants[battle.winner]["pokemon"]["name"]

    return {
        "battle": battle.to_dict(),
        "user_pok": user_pok,
        "rival_pok": rival_pok,
        "user_hp": battle.current_hp(0),
        "rival_hp": battle.current_hp(1),
        "logs": battle.log(),
        "is_over": battle.is_over(),
        "winner": battle.winner,
        "winner_trainer": winner_trainer,
        "winner_pokemon": winner_pokemon,
    }