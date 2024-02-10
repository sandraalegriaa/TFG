from dataclasses import dataclass
from typing import Protocol
import numpy as np
from jugadores import IJugador

@dataclass
class IMotorDeJuego(Protocol):
    """Clase interfaz de motor de juego"""

    _tablero: np.ndarray 
    _jugadorActivo: IJugador
    _jugador1: IJugador
    _jugador2: IJugador

    def getTablero(self) -> np.ndarray:
        return self._tablero
    
    def getJugadorActivo(self) -> IJugador:
        return self._jugadorActivo
    
    def getJugador1(self) -> IJugador:
        return self._jugador1
    
    def getJugador2(self) -> IJugador:
        return self._jugador2
    
    def setJugadorActivo(self,jugador):
        self._jugadorActivo = jugador