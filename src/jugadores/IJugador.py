from typing import Protocol
from dataclasses import dataclass

@dataclass
class IJugador(Protocol):
    """Clase Abstracta base del Jugador"""
    color: int
    turno: int

    def decideMovimiento(self):
        raise NotImplementedError()
    
    def getColor(self) -> str:
        raise NotImplementedError()
    
    def getTurno(self) -> int:
        raise NotImplementedError()
