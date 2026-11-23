class BattleError(Exception):
    """Excepción general para errores dentro de la batalla."""
    pass


class InvalidMoveError(BattleError):
    """Cuando se escoge un movimiento que no corresponde a su Pokémon."""
    pass


class BattleAlreadyOverError(BattleError):
    """Si se intenta lanzar un ataque cuando la batalla ya ha acabado."""
    pass