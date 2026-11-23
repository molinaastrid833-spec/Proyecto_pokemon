from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session
from app.forms.auth_forms import EntrenadorForm
from app.services import pokemon_service

auth_bp = Blueprint("auth", __name__)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer" not in session:
            return redirect(url_for("auth.inicio"))
        return func(*args, **kwargs)
    return wrapper


@auth_bp.route("/", methods=["GET", "POST"])
def inicio():
    if "trainer" in session:
        return redirect(url_for("pokemon.list_pokemon"))

    form = EntrenadorForm()
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    pokemon_destacado = pokemon_service.obtener_pokemon_destacado()

    if form.validate_on_submit():
        session["trainer"] = form.trainer.data.strip()
        return redirect(url_for("pokemon.list_pokemon"))

    return render_template(
        "index.html",
        form=form,
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        pokemon=pokemon_destacado
    )


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.inicio"))