from functools import wraps
import json
from pathlib import Path
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
from datetime import datetime
import random

'''es el obj que representa la app'''
app = Flask(__name__, template_folder = 'templates')

app.secret_key = "clave-secreta-pokemons-astrid"
# Guardar las sesiones en carpetas locales dentro del servidor
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

# 3. Inicializar la sesión en la aplicación
Session(app)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,  
    SESSION_COOKIE_SAMESITE="Lax"
)

'''La ruta se calcula desde este fichero, no desde donde se lance el programa'''
RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-ugly.json"

'''Leemos el JSON una sola vez, al iniciar la aplicación'''
with RUTA_DATOS.open("r", encoding="utf-8") as file:
    DATOS = json.load(file)


def login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer" not in session:
            return redirect(url_for("inicio"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET", "POST"])
def inicio():

    if request.method == "GET" and "trainer" in session:
        return redirect(url_for("list_pokemon"))

    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    pokemon = random.choice(DATOS)
    
    error = None
    trainer = ""
    
    if request.method == "POST":
        trainer = request.form.get("trainer", "").strip()
        
        if len(trainer) < 3 or len(trainer) > 15:
            error = "El nombre de entrenador debe tener entre 3 y 15 caracteres."
        else:
            session["trainer"] = trainer
            return redirect(url_for("list_pokemon"))
        
    return render_template("index.html", proyecto=proyecto, nombre=nombre, anho=anho, pokemon=pokemon, error= error, trainer= trainer)


@app.route("/pokemons", methods=["GET"])
@login # comprueba la sesion antes de entrar
def list_pokemon():

    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    trainer = session.get("trainer", "")
    
    nombre_pok = request.args.get("buscar_nombre", "").strip().lower()
    tipo = request.args.get("buscar_tipo", "").strip().lower()
    peso_min = request.args.get("peso_min", "").strip()
    
    lista_tipos = []
    for p in DATOS:
        for t in p["types"]:
            if t not in lista_tipos:
                lista_tipos.append(t)
                
    flitro_pokemon = []
    
    for p in DATOS:
        if nombre_pok and nombre_pok not in p["name"].lower():
            continue

        if tipo and tipo != "todos":
            tipos_min = [t.lower() for t in p["types"]]
            if tipo.lower() not in tipos_min:
                continue

        if peso_min and peso_min.isdigit():
            if p.get("weight", 0) < int(peso_min):
                continue

        flitro_pokemon.append(p)
    
    return render_template('poke.html',
        pokemons=flitro_pokemon, 
        proyecto=proyecto, 
        nombre=nombre, 
        anho=anho,
        trainer = trainer,
        tipos=lista_tipos,
        selected_nombre=nombre_pok,
        selected_tipo=tipo,
        selected_peso=peso_min,
        total_resultados=len(flitro_pokemon))

@app.route("/batalla")
@login
def batalla():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year

    pokemon_nombre = session.get("pokemon_batalla")

    batalla_sesion = session.get("batalla")

    if (not batalla_sesion) or (batalla_sesion.get("user_pok", {}).get("name", "").lower() != pokemon_nombre.lower()):

        user_pok = next((p for p in DATOS if p["name"].lower() == pokemon_nombre.lower()), None)
        if not user_pok:
            return redirect(url_for("list_pokemon"))

        rivales = [p for p in DATOS if p["name"].lower() != user_pok["name"].lower()]
        rival_pok = random.choice(rivales) if rivales else user_pok

        movimientos = user_pok.get("moves", user_pok.get("attacks", []))
        if len(movimientos) >= 4:
            ataques = random.sample(movimientos, 4)
        else:
            ataques = movimientos

        
        session["batalla"] = {
            "user_pok": user_pok,
            "rival_pok": rival_pok,
            "ataques": ataques
        }
    else:
        user_pok = batalla_sesion["user_pok"]
        rival_pok = batalla_sesion["rival_pok"]
        ataques = batalla_sesion["ataques"]

    return render_template(
        'batalla.html',
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        user_pok=user_pok,
        rival_pok=rival_pok,
        ataques=ataques
    )

@app.route("/preparar_batalla", methods=["GET", "POST"])
@login
def preparar_batalla():

    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    trainer = session.get("trainer", "")
       
    error = None
    
    if request.method == "POST":
        pokemon_elegido = request.form.get("pokemon_batalla", "").strip().lower()
        
        if not pokemon_elegido:
            error = "Debes escribir el nombre de un Pokemon."
        else:
            existe = any(p["name"].lower() == pokemon_elegido for p in DATOS)
            if existe:
                # Al seleccionar un Pokémon nuevo se invalida la batalla anterior
                session.pop("batalla", None)
                session["pokemon_batalla"] = pokemon_elegido
                return redirect(url_for("batalla"))
            else:
                error = f"El Pokémon ({pokemon_elegido}) no existe en el catálogo."


    return render_template('preparar_batalla.html', proyecto=proyecto, nombre=nombre, anho=anho, trainer = trainer, error=error)



@app.route("/pokemons/<int:id>")
@login
def detalles_pok(id):
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    trainer = session.get("trainer", "")
    
    for pokemon in DATOS:
        if int(pokemon["id"]) == id:
            return render_template(
                'detalles_pok.html',
                pokemon=pokemon,
                proyecto=proyecto, 
                nombre=nombre, 
                anho=anho
            )

    return "Pokémon no encontrado"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True, port= 8080)