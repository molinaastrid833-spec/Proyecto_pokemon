from datetime import datetime
from flask import Blueprint, render_template, request
from app.routes.auth_routes import login_required
from app.services import pokemon_service

pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.route("/pokemons", methods=["GET"])
@login_required
def list_pokemon():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year

    nombre_pok = request.args.get("buscar_nombre", "").strip().lower()
    tipo = request.args.get("buscar_tipo", "").strip().lower()
    peso_min = request.args.get("peso_min", "").strip()

    tipos = pokemon_service.obtener_lista_tipos()
    pokemons_filtrados = pokemon_service.filtrar_pokemons(nombre_pok, tipo, peso_min)

    return render_template(
        "poke.html",
        pokemons=pokemons_filtrados,
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        tipos=tipos,
        selected_nombre=nombre_pok,
        selected_tipo=tipo,
        selected_peso=peso_min,
        total_resultados=len(pokemons_filtrados)
    )


@pokemon_bp.route("/pokemons/<int:id>")
@login_required
def detalles_pok(id: int):
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year

    pokemon = pokemon_service.obtener_detalle(id)
    if not pokemon:
        return "Pokémon no encontrado", 404

    return render_template(
        "detalles_pok.html",
        pokemon=pokemon,
        proyecto=proyecto,
        nombre=nombre,
        anho=anho
    )