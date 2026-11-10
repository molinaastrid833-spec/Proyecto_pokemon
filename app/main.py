from flask import Flask
from flask_session import Session
from app.routes.auth_routes import auth_bp
from app.routes.pokemon_routes import pokemon_bp
from app.routes.battle_routes import battle_bp

app = Flask(__name__)

app.secret_key = "clave-secreta-pokemons-astrid"

# Configuración de sesiones persistentes en servidor
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

Session(app)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

# Registro de Blueprints de la capa de presentación
app.register_blueprint(auth_bp)
app.register_blueprint(pokemon_bp)
app.register_blueprint(battle_bp)

if __name__ == "__main__":
    app.run(debug=True, port=8080)