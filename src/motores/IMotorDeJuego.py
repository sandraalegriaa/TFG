from dataclasses import dataclass
from typing import Protocol
import numpy as np
from jugadores import IJugador
from interfaces import IInterfaz

@dataclass
class IMotorDeJuego(Protocol):
    """Clase interfaz de motor de juego"""

    _tablero: np.ndarray 
    _jugadorActivo: IJugador
    _jugador1: IJugador
    _jugador2: IJugador

    def getTablero(self) -> np.ndarray:
        raise NotImplementedError()
    
    def getJugadorActivo(self) -> IJugador:
        raise NotImplementedError()
    
    def getJugador1(self) -> IJugador:
        raise NotImplementedError()
    
    def getJugador2(self) -> IJugador:
        raise NotImplementedError()
    
    def setJugadorActivo(self,jugador):
        raise NotImplementedError()

    def getTablero(self) -> np.ndarray:
        raise NotImplementedError()
            
    def getJugadorActivo(self) -> IJugador:
        raise NotImplementedError()
    
    def getJugador1(self) -> IJugador:
        raise NotImplementedError()
            
    def getJugador2(self) -> IJugador:
        raise NotImplementedError()
            
    def setJugadorActivo(self,jugador: IJugador):
        raise NotImplementedError()
    
    def getFichasTablero(self) -> int:
        raise NotImplementedError()
            
    def _inicializarTablero (self):
        raise NotImplementedError()
            
    def obtenerValorCelda(self, fila:int, columna:int):
        raise NotImplementedError()
            
    def modificarValorCelda(self,fila:int,columna:int,valor:int):
        raise NotImplementedError()
            
    def dentroCeldas(self,fila:int,columna:int):
        raise NotImplementedError()
            
    def cambiarTurno(self, jugadorActual: IJugador):
        raise NotImplementedError()
            
    def juega(self, interfaz: IInterfaz):
        raise NotImplementedError()
            
    def obtenerJugadorContario(self,jugador:int):
        raise NotImplementedError()
            
    def obtenerValorContario(self,turno:int):
        raise NotImplementedError()
            
    def obtenerFichasJugador(self,jugador:IJugador) -> int:
        raise NotImplementedError()
            
    def aumentaCantidadFichasJugador(self,jugadorActivo:IJugador):
        raise NotImplementedError()
            
    def modificarCantidadFichasJugador(self, jugadorActivo: IJugador, cantidadFichas: int):
        raise NotImplementedError()
            
    def fichasContrariasEncerradas(self,filaColocacion:int,columnaColocacion:int,jugador: IJugador = None, contrario:IJugador = None):
        raise NotImplementedError()
            
    def cambiarValorFichasEncerradas(self,celdas):
        raise NotImplementedError()
            
    def comprobarFinJuego(self):
        raise NotImplementedError()
            
    def comprobarGanador(self):
        raise NotImplementedError()
            
    def comprobarPosiblesMovimientos(self):
        raise NotImplementedError()
            
    def posiblesMovimientos(self):
        raise NotImplementedError()
        
    def posiblesMovimientosJugador(self,jugador:IJugador):
        raise NotImplementedError()
        
    def colocarFicha(self,fila,columna,celdas):
        raise NotImplementedError()
        
    def obtenerEsquinasJugador(self,jugador:IJugador) -> int:
        raise NotImplementedError()

    def obtenerAdyacentesEsquinasJugador(self,jugador:IJugador) -> int:
        raise NotImplementedError()
        