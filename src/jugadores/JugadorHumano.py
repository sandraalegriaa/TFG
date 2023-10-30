from .Jugador import Jugador
from dataclasses import dataclass

@dataclass
class JugadorHumano(Jugador):
    """Clase del jugador humano"""

    def __init__(self, color, turno):
        self.color = color
        self.turno = turno