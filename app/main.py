import json
from pathlib import Path
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import random

'''es el obj que representa la app'''
app = Flask(__name__, template_folder = 'templates')
'''La ruta se calcula desde este fichero, no desde donde se lance el programa'''
RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-ugly.json"

'''Leemos el JSON una sola vez, al iniciar la aplicación'''
with RUTA_DATOS.open("r", encoding="utf-8") as file:
    DATOS = json.load(file)


@app.route("/", methods=["GET", "POST"])
def inicio():
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
            return redirect(url_for('list_pokemon', trainer=trainer))
        
    return render_template("index.html", proyecto=proyecto, nombre=nombre, anho=anho, pokemon=pokemon, error= error, trainer= trainer)


@app.route("/pokemons", methods=["GET"])
def list_pokemon():
    
    trainer = request.args.get("trainer")
    
    if not trainer:
        return redirect(url_for('inicio'))
    
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    
    
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
        trainer=trainer,
        tipos=lista_tipos,
        selected_nombre=nombre_pok,
        selected_tipo=tipo,
        selected_peso=peso_min,
        total_resultados=len(flitro_pokemon))

@app.route("/batalla")
def batalla():
    trainer = request.args.get("trainer")
    pokemon_nombre = request.args.get("pokemon")

    if not trainer or not pokemon_nombre:
        return redirect(url_for('inicio'))

    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year

    user_pok = None
    for p in DATOS:
        if p["name"].lower() == pokemon_nombre.lower():
            user_pok = p
            break

    if not user_pok:
        return redirect(url_for('list_pokemon', trainer=trainer))


    rivales = [p for p in DATOS if p["name"].lower() != user_pok["name"].lower()]
    rival_pok = random.choice(rivales) if rivales else user_pok


    movimientos = user_pok.get("moves", user_pok.get("attacks", []))
    if len(movimientos) >= 4:
        ataques = random.sample(movimientos, 4)
    else:
        ataques = movimientos

    return render_template(
        'batalla.html',
        proyecto=proyecto,
        nombre=nombre,
        anho=anho,
        trainer=trainer,
        user_pok=user_pok,
        rival_pok=rival_pok,
        ataques=ataques
    )

@app.route("/preparar_batalla", methods=["GET", "POST"])
def preparar_batalla():
    trainer = request.args.get("trainer")
    if not trainer:
        return redirect(url_for('inicio'))

    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
       
    error = None
    
    if request.method == "POST":
        pokemon_elegido = request.form.get("pokemon_batalla", "").strip().lower()
        
        if not pokemon_elegido:
            error = "Debes escribir el nombre de un Pokemon."
        else:
            existe = False
            for p in DATOS:
                if p["name"].lower() == pokemon_elegido:
                    existe = True
                    break
            
            if existe:
                return redirect(url_for('batalla', trainer=trainer, pokemon=pokemon_elegido))
            else: 
                error = f"El Pokemon ({pokemon_elegido}) no existe en el catalogo."


    return render_template('preparar_batalla.html', proyecto=proyecto, nombre=nombre, anho=anho, trainer=trainer, error=error)



@app.route("/pokemons/<int:id>")
def detalles_pok(id):
    trainer = request.args.get("trainer")
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = datetime.now().year
    for pokemon in DATOS:
        if int(pokemon["id"]) == id:

            return render_template(
                'detalles_pok.html',
                pokemon=pokemon,
                proyecto=proyecto, 
                nombre=nombre, 
                anho=anho,
                trainer=trainer
            )

    return "Pokémon no encontrado"


if __name__ == "__main__":
    app.run(debug=True, port= 8080)