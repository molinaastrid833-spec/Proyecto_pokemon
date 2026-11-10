from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PrepararBatallaForm(FlaskForm):
    pokemon_batalla = StringField(
        "Nombre del Pokémon",
        validators=[
            DataRequired(message="Debes escribir el nombre de un Pokémon.")
        ]
    )
    submit = SubmitField("Confirmar Selección")