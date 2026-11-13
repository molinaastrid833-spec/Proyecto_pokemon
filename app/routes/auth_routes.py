from functools import wraps
from datetime import datetime
import random
from flask import Blueprint, render_template, redirect, url_for, session
from app.forms.auth_forms import EntrenadorForm
from app.repositories.pokemon_repo import obtener_todos_pokemons

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
    
    # Obtener un Pokémon aleatorio para la portada desde la capa de datos
    todos = obtener_todos_pokemons()
    pokemon_destacado = random.choice(todos) if todos else None

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