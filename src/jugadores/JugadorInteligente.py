from dataclasses import dataclass

from motores import IMotorDeJuego
from jugadores import IJugador
import Constantes as c
import random
import copy

@dataclass
class JugadorInteligente():
    """Clase del jugador humano"""

    evaluador : int

    def __init__(self, color, turno,evaluador):
        self.color = color
        self.turno = turno
        self.evaluador = evaluador

    def getColor(self) -> str:
        return self.color
    
    def getTurno(self) -> int:
        return self.turno

    def evaluar(self, tablero):
        # Puntuaciones por posición
        puntajes = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100],
        ]

        # Inicializar puntuación
        puntuacion = 0

        # Identificar jugador y oponente
        jugador = self.turno

        # Evaluar cada celda del tablero
        for i in range(8):
            for j in range(8):
                if tablero[i][j] == jugador:
                    puntuacion += puntajes[i][j]
                elif tablero[i][j] != jugador and tablero[i][j] != 0:
                    puntuacion -= puntajes[i][j]

        # Devolver la puntuación total
        return puntuacion

    def evaluarEsquinas(self, tablero):
        #TODO: CAMBIAR
        puntuacion = 0
        peso_esquina = 20  # Peso asignado a las esquinas
        peso_borde = 10    # Peso asignado a los bordes
        peso_interior = 1  # Peso asignado a las piezas interiores

        # Dimensiones del tablero
        tamano = len(tablero)

        # Puntuaciones por posición en el tablero
        for i in range(tamano):
            for j in range(tamano):
                # Determinar el valor de la posición
                valor_posicion = peso_interior
                if (i == 0 or i == tamano - 1) and (j == 0 or j == tamano - 1):
                    valor_posicion = peso_esquina  # Es una esquina
                elif i == 0 or i == tamano - 1 or j == 0 or j == tamano - 1:
                    valor_posicion = peso_borde  # Es un borde

                # Actualizar la puntuación basada en el propietario de la pieza
                if tablero[i][j] == 1:  # Pieza negra
                    puntuacion -= valor_posicion
                elif tablero[i][j] == 2:  # Pieza blanca
                    puntuacion += valor_posicion

        # Añadir tu lógica para movilidad y estabilidad si lo deseas
        # Por ejemplo, podrías calcular el número de movimientos legales para cada jugador
        # y ajustar 'puntuacion' según quién tenga más opciones de jugar.

        return puntuacion

    def evaluarRandom(self,motor:IMotorDeJuego):
        """Evalua el movimiento de manera aleatoria"""

        return random.randint(-100, 100)
    
    def eligeMovimiento(self,motor:IMotorDeJuego):
        puntuacion, movimiento = self.minimax(motor,self,c.MAXIMA_PROFUNDIDAD_MINIMAX)
        return movimiento

    def minimax(self, motor, jugador, profundidad, alfa=float('-inf'), beta=float('inf')):
    
        #Comprobar fin de la recursión
        if profundidad == 0 or motor.comprobarFinJuego():
            if (self.evaluador == c.EVALUADOR_RANDOM):
                return self.evaluarRandom(motor.getTablero()), None
            elif (self.evaluador == c.EVALUADOR_ESQUINAS):
                return self.evaluarEsquinas(motor.getTablero()), None
            else: 
                return self.evaluar(motor.getTablero()), None
            
        #Incializar valores
        if motor.getJugadorActivo() == jugador:
            mejorPuntuacion = float('-inf')
        else:
            mejorPuntuacion = float('inf')

        mejorMovimiento = None

        for movimiento in motor.posiblesMovimientos():
            #Obtener fila,columna del movimiento
            fila, columna = movimiento[0], movimiento[1]

            #Duplicar motor de juego
            nuevoMotor = motor.__copy__()
            #Obtener fichas encerradas con el movimiento
            celdas = nuevoMotor.fichasContrariasEncerradas(fila, columna)
            #Colocar ficha en el nuevo motor de juego
            nuevoMotor.colocarFicha(fila, columna, celdas)

            #Aplicar recursión
            puntuacion, _ = self.minimax(nuevoMotor, jugador, profundidad - 1, alfa, beta)

            #Actualizar valores
            if motor.getJugadorActivo() == jugador:
                if puntuacion > mejorPuntuacion:
                    mejorPuntuacion = puntuacion
                    mejorMovimiento = movimiento
                beta = min(beta, puntuacion)
                if beta <= alfa:
                    break  # Poda alfa-beta
            else:
                if puntuacion < mejorPuntuacion:
                    mejorPuntuacion = puntuacion
                    mejorMovimiento = movimiento
                alfa = max(alfa, puntuacion)
                if alfa >= beta:
                    break  # Poda alfa-beta

        #Devolver valores obtenidos
        return mejorPuntuacion, mejorMovimiento