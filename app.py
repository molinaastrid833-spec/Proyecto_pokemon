from flask import Flask, render_template

'''es el obj que representa la app'''
app = Flask(__name__)

@app.route("/")
def inicio():
    proyecto = "Batallas Pokemon"
    nombre = "Astrid Molina"
    anho = 2026
    return render_template("index.html", proyecto=proyecto, nombre=nombre, anho=anho)