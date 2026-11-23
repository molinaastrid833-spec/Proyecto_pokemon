import random
from app.models.pokemon import Pokemon
from app.exceptions.exceptions import InvalidMoveError, BattleAlreadyOverError


class Battle:
    def __init__(self, participants: list[dict], turns: list[dict] | None = None, winner: int | None = None):
        self.participants = participants
        self.turns = turns if turns is not None else []
        self.winner = winner

    @classmethod
    def create(cls, user_trainer: str, user_pokemon: Pokemon, rival_pokemon: Pokemon) -> "Battle":
        """Crea una batalla nueva a partir de dos objetos Pokemon"""
        return cls(
            participants=[
                {
                    "trainer": user_trainer,
                    "pokemon": cls._build_battle_pokemon(user_pokemon),
                },
                {
                    "trainer": "CPU",
                    "pokemon": cls._build_battle_pokemon(rival_pokemon),
                },
            ],
            turns=[],
            winner=None,
        )

    @staticmethod
    def _build_battle_pokemon(pokemon: Pokemon) -> dict:
        data = pokemon.to_dict()
        base_hp = next((s["value"] for s in data["stats"] if s["name"] == "hp"), 50)
        data["max_hp"] = base_hp * 3

        # Solo 4 movimientos para el combate
        if len(data["moves"]) > 4:
            data["moves"] = random.sample(data["moves"], 4)

        return data

    def current_hp(self, participant: int) -> int:
        """Devuelve la vida actual del participante 0 o 1."""
        if participant not in (0, 1):
            raise ValueError("El participante debe estar entre 0 y 1.")

        for turn in reversed(self.turns):
            if turn["attacker"] != participant:
                return turn["remaining_hp"]

        return self.participants[participant]["pokemon"]["max_hp"]

    def is_over(self) -> bool:
        """Indica si la batalla ha finalizado."""
        return self.winner is not None

    def attack(self, move_name: str) -> None:
        """Ejecuta un turno completo: ataca el usuario y, solo si el rival sigue en pie, ataca el rival."""
        if self.is_over():
            raise BattleAlreadyOverError("La batalla ya ha terminado. Inicia una nueva partida para volver a combatir.")

        user_moves = self.participants[0]["pokemon"]["moves"]
        chosen_move = next(
            (m for m in user_moves if m["name"].lower() == move_name.strip().lower()),
            None,
        )

        if chosen_move is None:
            raise InvalidMoveError(f"El movimiento '{move_name}' no pertenece a tu Pokémon.")

        # 1) Ataca el usuario (0)
        self._execute_single_attack(attacker_idx=0, move=chosen_move)

        # 2) Si el rival sigue en pie, responde la CPU (1)
        if not self.is_over():
            cpu_moves = self.participants[1]["pokemon"]["moves"]
            if cpu_moves:
                cpu_move = random.choice(cpu_moves)
                self._execute_single_attack(attacker_idx=1, move=cpu_move)

    def _execute_single_attack(self, attacker_idx: int, move: dict) -> None:
        defender_idx = 1 - attacker_idx
        attacker_pok = self.participants[attacker_idx]["pokemon"]
        defender_pok = self.participants[defender_idx]["pokemon"]

        accuracy = move.get("accuracy")
        hit = True if accuracy is None else (random.randint(1, 100) <= accuracy)

        defender_hp = self.current_hp(defender_idx)
        damage = 0
        stab = False
        critical = False

        if hit:
            max_hp = defender_pok["max_hp"]
            base_damage = random.uniform(0.15, 0.30) * max_hp

            
            move_type = move.get("type", "").lower()
            attacker_types = [t.lower() for t in attacker_pok.get("types", [])]
            stab = move_type in attacker_types
            stab_multiplier = 1.20 if stab else 1.0

            # Escalado por potencia del movimiento y stats (attack vs defense)
            power = move.get("power") or 60
            power_factor = 0.90 + (min(power, 150) / 150) * 0.20  # entre 0.90 y 1.10

            atk_stat = self._get_stat(attacker_pok, "attack", 50)
            def_stat = self._get_stat(defender_pok, "defense", 50)
            stat_ratio = max(0.85, min(1.20, atk_stat / max(1, def_stat)))

            # Golpe crítico influido por la velocidad (speed)
            speed_stat = self._get_stat(attacker_pok, "speed", 50)
            crit_chance = min(0.30, 0.10 + (speed_stat / 1000))
            critical = random.random() < crit_chance
            crit_multiplier = 1.5 if critical else 1.0

            damage = max(1, round(base_damage * stab_multiplier * power_factor * stat_ratio * crit_multiplier))
            defender_hp = max(0, defender_hp - damage)

        turn_record = {
            "number": len(self.turns) + 1,
            "attacker": attacker_idx,
            "move": move["name"],
            "hit": hit,
            "damage": damage,
            "remaining_hp": defender_hp,
            "stab": stab,
            "critical": critical,
        }
        self.turns.append(turn_record)

        if defender_hp == 0:
            self.winner = attacker_idx

    @staticmethod
    def _get_stat(pokemon_data: dict, stat_name: str, default: int = 50) -> int:
        return next((s["value"] for s in pokemon_data.get("stats", []) if s["name"] == stat_name), default)

    def log(self) -> list[str]:
        
        entries = []
        for turn in self.turns:
            attacker_idx = turn["attacker"]
            defender_idx = 1 - attacker_idx
            attacker_name = self.participants[attacker_idx]["pokemon"]["name"].capitalize()
            defender_name = self.participants[defender_idx]["pokemon"]["name"].capitalize()
            prefix = "Tu" if attacker_idx == 0 else "El rival"

            if not turn["hit"]:
                entries.append(
                    f"Turno {turn['number']}: {prefix} {attacker_name} usó {turn['move']}, ¡pero falló el ataque!"
                )
            else:
                extras = []
                if turn.get("stab"):
                    extras.append("bonificación por mismo tipo")
                if turn.get("critical"):
                    extras.append("¡golpe crítico!")

                extra_text = f" ({', '.join(extras)})" if extras else ""
                entries.append(
                    f"Turno {turn['number']}: {prefix} {attacker_name} usó {turn['move']}{extra_text} "
                    f"e infligió {turn['damage']} puntos de daño a {defender_name} "
                    f"(PS restantes: {turn['remaining_hp']})."
                )

        return entries

    def to_dict(self) -> dict:
        return {
            "participants": self.participants,
            "turns": self.turns,
            "winner": self.winner,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Battle":
        return cls(
            participants=data["participants"],
            turns=data.get("turns", []),
            winner=data.get("winner"),
        )