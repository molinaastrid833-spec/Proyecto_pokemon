from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session
from app.routes.auth_routes import login_required
from app.forms.battle_forms import PrepararBatallaForm, AtacarForm
from app.services import battle_service
from app.exceptions.exceptions import BattleError

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

        if battle_service.existe_pokemon_para_batalla(pokemon_elegido):
            session.pop("battle", None)
            session["pokemon_batalla"] = pokemon_elegido
            return redirect(url_for("battle.battle"))
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


@battle_bp.route("/battle", methods=["GET", "POST"])
@login_required
def battle():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year

    pokemon_nombre = session.get("pokemon_batalla")
    if not pokemon_nombre:
        return redirect(url_for("battle.preparar_batalla"))

    batalla_sesion = session.get("battle")

    # Si no hay batalla en curso o se cambió de Pokémon, iniciamos una nueva
    if (
        not batalla_sesion
        or batalla_sesion["participants"][0]["pokemon"]["name"].lower() != pokemon_nombre.lower()
    ):
        batalla_sesion = battle_service.iniciar_batalla(session["trainer"], pokemon_nombre)
        if not batalla_sesion:
            return redirect(url_for("pokemon.list_pokemon"))
        session["battle"] = batalla_sesion

    form = AtacarForm()
    error = None

    if form.validate_on_submit():
        try:
            batalla_actualizada = battle_service.ejecutar_turno(
                batalla_sesion,
                form.move_name.data
            )
            session["battle"] = batalla_actualizada
            return redirect(url_for("battle.battle"))
        except BattleError as e:
            error = str(e)

    resumen = battle_service.obtener_resumen_batalla(session["battle"])

    return render_template(
        "batalla.html",
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        form=form,
        error=error,
        **resumen
    )


@battle_bp.route("/nueva_batalla", methods=["POST"])
@login_required
def nueva_batalla():
    session.pop("battle", None)
    return redirect(url_for("battle.battle"))