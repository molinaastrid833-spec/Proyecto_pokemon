import json
from pathlib import Path
from flask import Flask, render_template
from datetime import datetime
import random

'''es el obj que representa la app'''
app = Flask(__name__)
'''La ruta se calcula desde este fichero, no desde donde se lance el programa'''
RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-ugly.json"

'''Leemos el JSON una sola vez, al iniciar la aplicación'''
with RUTA_DATOS.open("r", encoding="utf-8") as file:
    DATOS = json.load(file)


@app.route("/")
def inicio():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    pokemon = random.choice(DATOS)
    return render_template("index.html", proyecto=proyecto, nombre=nombre, anho=anho, pokemon=pokemon)


@app.route("/pokemons")
def list_pokemon():
    return render_template('poke.html', pokemons=DATOS)


@app.route("/pokemons/<int:id>")
def detalles_pok(id):
    for pokemon in DATOS:
        if int(pokemon["id"]) == id:
            peso = pokemon["weight"]

            if peso < 100:
                categoria_peso = "Ligero"
            elif peso <= 500:
                categoria_peso = "Normal"
            else:
                categoria_peso = "Pesado"

            return render_template(
                'detalles_pok.html',
                pokemon=pokemon,
                categoria_peso=categoria_peso
            )

    return "Pokémon no encontrado"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= 8080)