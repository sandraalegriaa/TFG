from dataclasses import dataclass, Field
from typing import Protocol

import numpy as np

import Constantes as c

from interfaces import IInterfaz

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
        
        if (self._dentroCeldas):
            return self._tablero[fila][columna]
        
        return None
    
    def modificarValorCelda(self,fila,columna,valor):
        """Modificar el valor de una celda en el tablero"""
        
        self._tablero[fila][columna] = valor

    
    def dentroCeldas(self, fila,columna):
        """Comprueba si una celda se encuentra en el tablero"""

        return fila in range(0,8) and columna in range(0,8)
    
    def juega(self, interfaz: IInterfaz):
        """Inicia el juego (incluida la inicialización del tablero)"""

        self._inicializarTablero(interfaz)

        while(True):
            interfaz.gestionEventos()

    

    

