from app.models.pokemon import Pokemon
from app.repositories.pokemon_repo import obtener_todos_pokemons, buscar_por_id, buscar_por_nombre


def obtener_lista_tipos() -> list[str]:
    tipos = []
    for pokemon in obtener_todos_pokemons():
        for t in pokemon.types:
            if t not in tipos:
                tipos.append(t)
    return tipos


def filtrar_pokemons(nombre_pok: str = "", tipo: str = "", peso_min: str = "") -> list[Pokemon]:
    pokemons = obtener_todos_pokemons()
    resultado = []

    for p in pokemons:
        if nombre_pok and nombre_pok not in p.name.lower():
            continue

        if tipo and tipo != "todos":
            tipos_min = [t.lower() for t in p.types]
            if tipo.lower() not in tipos_min:
                continue

        if peso_min and peso_min.isdigit():
            if p.weight < int(peso_min):
                continue

        resultado.append(p)

    return resultado


def obtener_detalle(pokemon_id: int) -> Pokemon | None:
    return buscar_por_id(pokemon_id)