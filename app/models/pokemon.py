class Pokemon:
    
    def __init__(self, id, name, height, weight, types, stats, moves, sprites):
        self.id = int(id)
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.stats = stats
        self.moves = moves
        self.sprites = sprites

    @property
    def categoria_peso(self) -> str:
        if self.weight < 100:
            return "Ligero"
        elif self.weight <= 500:
            return "Normal"
        return "Pesado"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "types": self.types,
            "stats": self.stats,
            "moves": self.moves,
            "sprites": self.sprites,
        }