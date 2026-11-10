from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session
from app.routes.auth_routes import login_required
from app.forms.battle_forms import PrepararBatallaForm
from app.services import battle_service
from app.repositories.pokemon_repo import buscar_por_nombre

battle_bp = Blueprint("battle", __name__)


@battle_bp.route("/preparar_batalla", methods=["GET", "POST"])
@login_required
def preparar_batalla():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    
    form = PrepararBatallaForm()
    error = None

    if form.validate_on_submit():
        pokemon_elegido = form.pokemon_batalla.data.strip().lower()
        existe = buscar_por_nombre(pokemon_elegido)
        
        if existe:
            session.pop("batalla", None)
            session["pokemon_batalla"] = pokemon_elegido
            return redirect(url_for("battle.batalla"))
        else:
            error = f"El Pokémon ({pokemon_elegido}) no existe en el catálogo."

    return render_template(
        "preparar_batalla.html",
        form=form,
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        error=error
    )


@battle_bp.route("/batalla")
@login_required
def batalla():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year

    pokemon_nombre = session.get("pokemon_batalla")
    if not pokemon_nombre:
        return redirect(url_for("battle.preparar_batalla"))

    batalla_sesion = session.get("batalla")

    if (not batalla_sesion) or (batalla_sesion.get("user_pok", {}).get("name", "").lower() != pokemon_nombre.lower()):
        datos_combate = battle_service.preparar_combate(pokemon_nombre)
        if not datos_combate:
            return redirect(url_for("pokemon.list_pokemon"))

        session["batalla"] = datos_combate
        user_pok = datos_combate["user_pok"]
        rival_pok = datos_combate["rival_pok"]
        ataques = datos_combate["ataques"]
    else:
        user_pok = batalla_sesion["user_pok"]
        rival_pok = batalla_sesion["rival_pok"]
        ataques = batalla_sesion["ataques"]

    return render_template(
        "batalla.html",
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        user_pok=user_pok,
        rival_pok=rival_pok,
        ataques=ataques
    )