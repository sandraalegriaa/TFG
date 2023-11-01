from dataclasses import dataclass, Field
from typing import Protocol

import numpy as np

import Constantes as c

from interfaces import IInterfaz
from jugadores import Jugador

@dataclass
class MotorDeJuego ():
    _tablero = np.zeros((8, 8))

    def __init__(self, jugador1, jugador2):

        self._jugador1 = jugador1
        self._jugador2 = jugador2

        #Realiza el primer movimiento el que maneje a las fichas negras
        if self._jugador1.getColor() == c.NEGRO:
            self._jugadorActivo = self._jugador1
        else: 
            self._jugadorActivo = self._jugador2

    def getTablero(self) -> np.ndarray:
        """Devuelve el tablero de juego del motor de juego"""

        return self._tablero
    
    def getJugadorActivo(self) -> Jugador:
        """Devuelve el jugador activo del motor de juego"""

        return self._jugadorActivo
    
    def getJugador1(self) -> Jugador:
        """Devuelve el jugador1 del motor de juego"""

        return self._jugador1
    
    def getJugador2(self) -> Jugador:
        """Devuelve el jugador2 del motor de juego"""

        return self._jugador2
    
    def setJugadorActivo(self,jugador):
        """Cambiar el jugador activo en el motor de juego"""

        self._jugadorActivo = jugador

    def _inicializarTablero (self, interfaz):
        """Iniciliza el tablero de juego siguiendo las reglas estándar y actualiza la interfaz"""

        #Fichas blancas
        self._tablero[3][c.D] = 2
        self._tablero[4][c.E] = 2

        #Fichas negras
        self._tablero[4][c.D] = 1
        self._tablero[3][c.E] = 1

        #Actualizar interfaz
        interfaz.inicializarInterfaz()

    def obtenerValorCelda(self, fila, columna):
        """Obtener el valor de una celda en el tablero"""
        
        if (self.dentroCeldas(fila,columna)):
            return self._tablero[fila][columna]
        
        return None
    
    def modificarValorCelda(self,fila,columna,valor):
        """Modificar el valor de una celda en el tablero"""
        
        self._tablero[fila][columna] = valor

    
    def dentroCeldas(self,fila,columna):
        """Comprueba si una celda se encuentra en el tablero"""

        return fila in range(0,8) and columna in range(0,8)
    
    def cambiarTurno(self, jugadorActual):
        """Cambiar el jugador activo dando el turno al siguiente jugador"""

        if jugadorActual.getTurno() == c.P1:
            self.setJugadorActivo(self._jugador2)
            print("Cambio de turno a jugador 2")
        else: 
            self.setJugadorActivo(self._jugador1)
            print("Cambio de turno a jugador 1")      
    
    def juega(self, interfaz: IInterfaz):
        """Inicia el juego (incluida la inicialización del tablero)"""

        self._inicializarTablero(interfaz)

        while(True):
            interfaz.gestionEventos(self)

    def adyacencia (self,fila,columna):
        """Comprueba la adyacencia de la celda seleccionada por el jugador activo con las fichas del rival en las ocho posibles direcciones (a una celda de distancia)"""

        adyp2 = False
        adyp1 = False

        adyacente = False
        
        #Borde superior del tablero
        if (not ((fila-1) < 0)):
            adyp2 = self._tablero[fila-1][columna] == c.P2
            adyp1 = self._tablero[fila-1][columna] == c.P1
            #Esquina superior izquierda
            if (not ((columna - 1) < 0)):
                adyp2 = adyp2 or self._tablero[fila-1][columna-1] == c.P2
                adyp1 = adyp1 or self._tablero[fila-1][columna-1] == c.P1
            #Esquina superior izquierda
            if (not ((columna + 1) >= c.CELDAS)):
                adyp2 = adyp2 or self._tablero[fila-1][columna+1] == c.P2
                adyp1 = adyp1 or self._tablero[fila-1][columna+1] == c.P1
        
        #Borde inferior del tablero
        if (not ((fila + 1) >= c.CELDAS)):
            adyp2 = adyp2 or self._tablero[fila+1][columna] == c.P2 
            adyp1 = adyp1 or self._tablero[fila+1][columna] == c.P1 
            #Esquina inferior izquierda
            if (not ((columna - 1) < 0)):
                adyp2 = adyp2 or self._tablero[fila+1][columna-1] == c.P2
                adyp1 = adyp1 or self._tablero[fila+1][columna-1] == c.P1
            #Esquina inferior derecha
            if (not ((columna + 1) >= c.CELDAS)):
                adyp2 = adyp2 or self._tablero[fila+1][columna+1] == c.P2
                adyp1 = adyp1 or self._tablero[fila+1][columna+1] == c.P1

        #Borde izquierdo del tablero
        if (not ((columna - 1) < 0)):
            adyp2 = adyp2 or self._tablero[fila][columna-1] == c.P2
            adyp1 = adyp1 or self._tablero[fila][columna-1] == c.P1
        #Borde derecho del tablero
        if (not ((columna + 1) >= c.CELDAS)):
            adyp2 = adyp2 or self._tablero[fila][columna+1] == c.P2
            adyp1 = adyp1 or self._tablero[fila][columna+1] == c.P1

        if (self._jugadorActivo.getTurno() == c.P1 and adyp2):
            adyacente = True
        elif (self._jugadorActivo.getTurno() == c.P2 and adyp1):
            adyacente = True

        return adyacente

    

    

