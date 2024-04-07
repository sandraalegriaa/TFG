from dataclasses import dataclass

@dataclass
class Jugador ():
    """Clase del jugador humano"""

    _color: str
    _turno: int

    def getColor(self) -> str:
        return self._color
    
    def getTurno(self) -> int:
        return self._turno

    