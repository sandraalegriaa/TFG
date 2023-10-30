from typing import Protocol
from dataclasses import dataclass

@dataclass
class Jugador(Protocol):
    """Clase Abstracta base del Jugador"""
    color: int
    turno: int

    def decideMovimiento(self):
        raise NotImplementedError()
    
    def getColor(self) -> str:
        return self.color
    
    def getTurno(self) -> int:
        return self.turno
