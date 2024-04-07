from dataclasses import dataclass
from jugadores.Jugador import Jugador

@dataclass
class JugadorHumano(Jugador):
    """Clase del jugador humano"""

    def __init__(self, color, turno):
        super().__init__(color,turno)

    