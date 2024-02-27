from dataclasses import dataclass, Field
from typing import Protocol

import numpy as np

import Constantes as c

from interfaces import IInterfaz
from jugadores import IJugador

@dataclass
class MotorDeJuego ():

    _tablero = np.zeros((8, 8))

    _jugador1: IJugador
    _jugador2: IJugador

    _fichasNegras: int
    _fichasBlancas: int

    _posibleMovimientoJ1: bool
    _posibleMovimientoJ2: bool

    def __init__(self, jugador1, jugador2, tablero=None, fichasNegras=None, fichasBlancas=None, puedeMoverJ1= None, puedeMoverJ2 = None,tableroCompletado = None, jugadorActivo = None):

        if tablero is not None:
            # Usar tablero proporcionado
            self._tablero = tablero
        else:
            # Inicializar un tablero
            self._inicializarTablero()

        self._jugador1 = jugador1
        self._jugador2 = jugador2

        #Ambos jugadores pueden comenzar realizando movimientos 
        if puedeMoverJ1 is not None:
            # Usar valor proporcionado
            self._posibleMovimientoJ1 = puedeMoverJ1
        else: 
            # Inicializar valor
            self._posibleMovimientoJ1 = True

        if puedeMoverJ2 is not None:
            # Usar valor proporcionado
            self._posibleMovimientoJ2 = puedeMoverJ2
        else:
            # Inicializar valor
            self._posibleMovimientoJ2 = True

        
        if tableroCompletado is not None:
            # Usar valor proporcionado
            self._tableroCompletado = tableroCompletado
        else:
            #El tablero comienza con huecos disponibles
            self._tableroCompletado = False

        #Inicializar la cantidad de fichas de cada jugador según las reglas de inicialización del tablero
        if fichasNegras is not None:
            # Usar valor proporcionado
            self._fichasNegras = fichasNegras
        else:
            # Inicializar valor
            self._fichasNegras = 2

        if fichasBlancas is not None:
            # Usar valor proporcionado
            self._fichasBlancas = fichasBlancas
        else:
            # Inicializar valor
            self._fichasBlancas = 2

        if jugadorActivo is not None:
            # Usar valor proporcionado
            self._jugadorActivo = jugadorActivo
        else:
            #Realiza el primer movimiento el que maneje a las fichas negras
            if self._jugador1.getColor() == c.NEGRO:
                self._jugadorActivo = self._jugador1
            else: 
                self._jugadorActivo = self._jugador2

    def getTablero(self) -> np.ndarray:
        """Devuelve el tablero de juego del motor de juego"""

        return self._tablero
    
    def getJugadorActivo(self) -> IJugador:
        """Devuelve el jugador activo del motor de juego"""

        return self._jugadorActivo
    
    def getJugador1(self) -> IJugador:
        """Devuelve el jugador1 del motor de juego"""

        return self._jugador1
    
    def getJugador2(self) -> IJugador:
        """Devuelve el jugador2 del motor de juego"""

        return self._jugador2
    
    def setJugadorActivo(self,jugador: IJugador):
        """Cambiar el jugador activo en el motor de juego"""

        self._jugadorActivo = jugador

    def _inicializarTablero (self):
        """Iniciliza el tablero de juego siguiendo las reglas estándar"""

        #Fichas blancas
        self._tablero[3][c.D] = 2
        self._tablero[4][c.E] = 2

        #Fichas negras
        self._tablero[4][c.D] = 1
        self._tablero[3][c.E] = 1

    def obtenerValorCelda(self, fila:int, columna:int):
        """Obtener el valor de una celda en el tablero"""
        
        if (self.dentroCeldas(fila,columna)):
            return self._tablero[fila][columna]
        
        return None
    
    def modificarValorCelda(self,fila:int,columna:int,valor:int):
        """Modificar el valor de una celda en el tablero"""
        
        self._tablero[fila][columna] = valor

    
    def dentroCeldas(self,fila:int,columna:int):
        """Comprueba si una celda se encuentra en el tablero"""

        return fila in range(0,8) and columna in range(0,8)
    
    def cambiarTurno(self, jugadorActual: IJugador):
        """Cambiar el jugador activo dando el turno al siguiente jugador"""

        if jugadorActual.getTurno() == c.P1:
            self.setJugadorActivo(self._jugador2)
            #print("Cambio de turno a jugador 2")
        else: 
            self.setJugadorActivo(self._jugador1)
            #print("Cambio de turno a jugador 1")      
    
    def juega(self, interfaz: IInterfaz):
        """Inicia el juego (incluida la inicialización del tablero)"""

        #TODO: BORRAR self._inicializarTablero(interfaz)

        while(True):
            interfaz.gestionEventos(self)
    
    def obtenerValorContario(self,turno:int):
        """Obtener el valor de turno del contrario"""
        
        if turno == c.P1:
            contrario = c.P2
        else: 
            contrario = c.P1

        return contrario

    def aumentaCantidadFichasJugador(self,jugadorActivo:IJugador):
        """Incrementa en 1 la cantidad de fichas de un jugador al colocar una ficha"""

        if jugadorActivo.getTurno() == c.P1:
            self._fichasNegras += 1
        else: 
            self._fichasBlancas += 1

    def modificarCantidadFichasJugador(self, jugadorActivo: IJugador, cantidadFichas: int):
        """Modifica la cantidad de fichas de un jugador al encerrar fichas de su oponente"""

        if jugadorActivo.getTurno() == c.P1:
            self._fichasNegras += cantidadFichas
            self._fichasBlancas -= cantidadFichas
        else: 
            self._fichasBlancas += cantidadFichas
            self._fichasNegras -= cantidadFichas
        
        #TODO: BORRAR
        
        print(self._fichasNegras,self._fichasBlancas)

    def fichasContrariasEncerradas(self,filaColocacion:int,columnaColocacion:int):
        """Determinar que celdas han sido encerradas tras la colocación y cambiar su valor"""
        celdasEncerradas = []
        celdas = []

        valorContrario = self.obtenerValorContario(self.getJugadorActivo().getTurno())
        valorJugador = self.getJugadorActivo().getTurno()

        # Rectas
        # Arriba, Abajo, Izquierda, Derecha, DiagonalArribaIzquierda, DiagonalArribaDerecha, DiagonalAbajoIzquierda, DiagonalAbajoDerecha
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0),(-1, -1),(-1, 1),(1, -1),(1, 1)]  
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

    def comprobarFinJuego(self):
        """Comprobar si el juego se ha acabado porque:
          - No quedan casillas libres en el tablero. 
          - Ningún jugador puede realizar movimientos."""
        
        fin = False

        if(self._fichasNegras+self._fichasBlancas >= c.CASILLAS_TABLERO):
            fin = True
        elif(not self._posibleMovimientoJ1 and not self._posibleMovimientoJ2):
            fin = True

        return fin 
    
    def comprobarGanador(self):
        """Comprobar qué jugador es el ganador o si ha habido empate"""
        
        ganador = None

        if (self._fichasNegras == self._fichasBlancas):
            ganador = c.EMPATE_ENTRE_JUGADORES
        elif (self._fichasNegras > self._fichasBlancas):
            ganador = c.JUGADOR1_GANA
        else:
            ganador = c.JUGADOR2_GANA

        return ganador
    
    def comprobarPosiblesMovimientos(self):
        """Recorrer el tablero buscando si hay posibles movimientos para el jugador activo"""
        posible = False

        #Recorrer tablero comprobando cada celda
        for fila in range(c.CELDAS):
            for columna in range(c.CELDAS):
                if (self.obtenerValorCelda(fila,columna) == 0):
                    encerradas = self.fichasContrariasEncerradas(fila,columna)
                    if (len(encerradas) > 0):
                        posible = True
                        break

        #Almacenar información
        if self._jugadorActivo.getTurno() == c.P1:
            self._posibleMovimientoJ1 = posible
        else: 
            self._posibleMovimientoJ2 = posible
        
        return posible
    
    def posiblesMovimientos(self):
        """Recorrer el tablero buscando los posibles movimientos para el jugador activo"""
        movimientos = []

        #Recorrer tablero comprobando cada celda
        for fila in range(c.CELDAS):
            for columna in range(c.CELDAS):
                if (self.obtenerValorCelda(fila,columna) == 0):
                    encerradas = self.fichasContrariasEncerradas(fila,columna)
                    if (len(encerradas) > 0):
                        movimientos.append((fila,columna))

        return movimientos
    
    def colocarFicha(self,fila,columna,celdas):
        """Colocar ficha del jugador activo en el tablero"""
        self.modificarValorCelda(fila,columna,self.getJugadorActivo().getTurno())
        self.aumentaCantidadFichasJugador(self.getJugadorActivo())
        
        #Capturar fichas enemigas
        self.cambiarValorFichasEncerradas(celdas)

        self.modificarCantidadFichasJugador(self.getJugadorActivo(), len(celdas))

        #Turno del siguiente jugador
        self.cambiarTurno(self.getJugadorActivo())
    
    def __copy__(self):
        nuevoMotor = MotorDeJuego(self._jugador1,self._jugador2,np.copy(self._tablero),self._fichasNegras,self._fichasBlancas,self._posibleMovimientoJ1,self._posibleMovimientoJ2,self._tableroCompletado)
        return nuevoMotor