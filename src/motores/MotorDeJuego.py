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
    
    def obtenerValorContario(self,turno):
        """Obtener el valor de turno del contrario"""
        
        if turno == c.P1:
            contrario = c.P2
        else: 
            contrario = c.P1

        return contrario

    def posibleColocacion(self,fila,columna):
        """Comprueba si la colocación es posible:
            - True cuando se encierran fichas
            - False en caso contrario
        """

        valorContrario = self.obtenerValorContario(self.getJugadorActivo().getTurno())
        valorJugador = self.getJugadorActivo().getTurno()

        # Arriba, Abajo, Izquierda, Derecha, DiagonalArribaIzquierda, DiagonalArribaDerecha, DiagonalAbajoIzquierda, DiagonalAbajoDerecha
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0),(-1, -1),(-1, 1),(-1, 1),(1, 1)]  
        for dx, dy in direcciones:
            celdas = []
            x, y = fila, columna
            while True:
                x += dx
                y += dy
                if x < 0 or x >= c.CELDAS or y < 0 or y >= c.CELDAS:
                    break
                valor = self.obtenerValorCelda(x, y)
                if valor == valorContrario:
                    celdas.append([x, y])
                elif valor == valorJugador:
                    if len(celdas) > 0:
                        return True
                elif valor == 0:
                    break

        return False

    def fichasContrariasEncerradas(self,filaColocacion,columnaColocacion):
        """Determinar que celdas han sido encerradas tras la colocación y cambiar su valor"""
        celdasEncerradas = []
        celdas = []

        print()
        print("FICHAS ENCERRADAS")
        print() 
        print(f"filaColocacion= {filaColocacion}, columnaColocacion={columnaColocacion}")

        valorContrario = self.obtenerValorContario(self.getJugadorActivo().getTurno())
        valorJugador = self.getJugadorActivo().getTurno()

        print(f"valorContarior= {valorContrario}, valorJugador={valorJugador}")
        print()

        # Rectas
        # Arriba, Abajo, Izquierda, Derecha, DiagonalArribaIzquierda, DiagonalArribaDerecha, DiagonalAbajoIzquierda, DiagonalAbajoDerecha
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0),(-1, -1),(-1, 1),(-1, 1),(1, 1)]  
        for dx, dy in direcciones:
            celdas = []
            x, y = filaColocacion, columnaColocacion
            while True:
                x += dx
                y += dy
                if x < 0 or x >= c.CELDAS or y < 0 or y >= c.CELDAS:
                    break
                valor = self.obtenerValorCelda(x, y)
                if valor == valorContrario:
                    celdas.append([x, y])
                elif valor == valorJugador:
                    celdasEncerradas.extend(celdas)
                    break
                elif valor == 0:
                    break

        return celdasEncerradas

    def cambiarValorFichasEncerradas(self,celdas):
        for celda in celdas:
            fila, columna = celda[0], celda[1]
            valor = self.obtenerValorCelda(fila,columna)
            self.modificarValorCelda(fila,columna,self.obtenerValorContario(valor))