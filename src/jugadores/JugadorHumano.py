from dataclasses import dataclass

@dataclass
class JugadorHumano():
    """Clase del jugador humano"""

    def __init__(self, color, turno):
        self.color = color
        self.turno = turno

    def getColor(self) -> str:
        return self.color
    
    def getTurno(self) -> int:
        return self.turno

    