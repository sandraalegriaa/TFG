from dataclasses import dataclass
from typing import Protocol
import numpy as np
from jugadores import Jugador

@dataclass
class IMotorDeJuego(Protocol):
    """Clase interfaz de motor de juego"""

    _tablero: np.ndarray 
    _jugadorActivo: Jugador
    _jugador1: Jugador
    _jugador2: Jugador

    def getTablero(self) -> np.ndarray:
        return self._tablero
    
    def getJugadorActivo(self) -> Jugador:
        return self._jugadorActivo
    
    def getJugador1(self) -> Jugador:
        return self._jugador1
    
    def getJugador2(self) -> Jugador:
        return self._jugador2
    
    def setJugadorActivo(self,jugador):
        self._jugadorActivo = jugador