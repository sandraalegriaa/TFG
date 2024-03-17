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
    
    def cambiarEvaluador(self, evaluador:int):
        self.evaluador = evaluador

    #Funciones de evaluación
    def evaluarRandom(self,motor:IMotorDeJuego):
        """Evalua el movimiento de manera aleatoria"""

        return random.randint(c.MIN_PUNTUACION, c.MAX_PUNTUACION)
    
    def evaluarFichas(self,motor:IMotorDeJuego,jugador:IJugador):
        """Evalua el movimiento en función del número de fichas de los jugadores, cuantas más fichas mejor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        fichasJugador = motor.obtenerFichasJugador(jugador)
        fichasContrario = motor.obtenerFichasJugador(jugadorContrario)

        if (fichasJugador > fichasContrario):
            puntuacion = c.MAX_PUNTUACION
        elif (fichasJugador < fichasContrario):
            puntuacion = c.MIN_PUNTUACION
        else:
            puntuacion = c.EMPATE_PUNTUACION

        return puntuacion
    
    def evaluarMovilidad(self,motor:IMotorDeJuego,jugador:IJugador):
        """Evalua el movimiento en función del número del número de movimientos posibles, cuantos más movimientos mejor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        movimientosJugador = len(motor.posiblesMovimientosJugador(jugador))
        movimientosContrario = len(motor.posiblesMovimientosJugador(jugadorContrario))

        if (movimientosJugador + movimientosContrario != 0):
            puntuacion = 100*(movimientosJugador-movimientosContrario)/(movimientosJugador+movimientosContrario)
        else:
            puntuacion = 0

        return puntuacion
    
    def evaluarEsquinas(self,motor:IMotorDeJuego,jugador:IJugador):
        """Evalua el movimiento en función del número del número esquinas ocupadas con fichas del jugador, cuantos más esquinas mejor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        esquinasJugador = motor.obtenerEsquinasJugador(jugador)
        esquinasContrario = motor.obtenerEsquinasJugador(jugadorContrario)

        if (esquinasJugador + esquinasContrario != 0):
            puntuacion = 100*(esquinasJugador-esquinasContrario)/(esquinasJugador+esquinasContrario)
        else:
            puntuacion = 0

        return puntuacion

    def evaluarCombinado(self, motor:IMotorDeJuego, jugador:IJugador):
        """Evalúa combinando el número de fichas, la movilidad y las esquinas ocupadas,dando el mismo peso a cada evaluación."""

        #Comprobar porcentaje de la partida
        fichasTablero = motor.getFichasTablero()
        porcentaje = 100 * (fichasTablero/c.CASILLAS_TABLERO)

        if porcentaje == 100:
            puntuacion = self.evaluarFichas(motor, jugador)
        else:
            #Obtener puntuciones
            puntuacionMovilidad = self.evaluarMovilidad(motor, jugador)
            puntuacionEsquinas = self.evaluarEsquinas(motor, jugador)

            #Calcular multiplicadores para los evaluadores
            if (porcentaje >= c.PORCENTAJES_MOVILIDAD['min'] and porcentaje <= c.PORCENTAJES_MOVILIDAD['max']):
                multiplicador =  c.VALOR_EVALUADOR_MOVILIDAD
            else:
                multiplicador = 100 - c.VALOR_EVALUADOR_MOVILIDAD

            puntuacionMovilidad = puntuacionMovilidad * multiplicador

            if (porcentaje > c.PORCENTAJES_ESQUINAS['min'] and porcentaje < c.PORCENTAJES_ESQUINAS['max']):
                multiplicador =  c.VALOR_EVALUADOR_ESQUINAS
            else:
                multiplicador = 100 - c.VALOR_EVALUADOR_ESQUINAS

            puntuacionEsquinas = puntuacionEsquinas * multiplicador
        
            # Calcular la puntuación total
            puntuacion = puntuacionMovilidad + puntuacionEsquinas
        
        return puntuacion
    
    def evaluarPesoCasillas(self, motor:IMotorDeJuego, jugador:IJugador):
        """Calcula el valor de utilidad para un jugador basado en los pesos de cada casilla."""

        jugadorContrario = motor.obtenerJugadorContario(jugador)
        puntuacionJugador = 0
        puntuacionContrario = 0
        
        # Sumar los pesos de las posiciones de las fichas de cada jugador
        for fila in range(c.CELDAS):
            for columna in range(c.CELDAS):
                if motor.obtenerValorCelda(fila, columna) == jugador.getColor():
                    puntuacionJugador += c.PESOS_TABLERO[fila][columna]
                elif motor.obtenerValorCelda(fila, columna) == jugadorContrario.getColor():
                    puntuacionContrario += c.PESOS_TABLERO[fila][columna]

        # Calcular la puntuacion final
        puntuacion = puntuacionJugador - puntuacionContrario
        
        return puntuacion

    def eligeMovimiento(self,motor:IMotorDeJuego):
        puntuacion, movimiento = self.minimax(motor,self,c.MAXIMA_PROFUNDIDAD_MINIMAX)
        return movimiento

    #Minimax
    def minimax(self, motor:IMotorDeJuego, jugador: IJugador, profundidad:int, alfa=float('-inf'), beta=float('inf')):
    
        #Comprobar fin de la recursión
        if profundidad == 0 or motor.comprobarFinJuego():
            if (self.evaluador == c.EVALUADOR_RANDOM):
                return self.evaluarRandom(motor), None
            elif (self.evaluador == c.EVALUADOR_FICHAS):
                return self.evaluarFichas(motor,jugador), None
            elif (self.evaluador == c.EVALUADOR_MOVILIDAD):
                return self.evaluarMovilidad(motor,jugador), None
            elif (self.evaluador == c.EVALUADOR_ESQUINAS):
                return self.evaluarEsquinas(motor,jugador), None
            elif (self.evaluador == c.EVALUADOR_COMBINADO):
                return self.evaluarCombinado(motor,jugador), None
            elif (self.evaluador == c.EVALUADOR_PESOS):
                return self.evaluarPesoCasillas(motor,jugador), None
                        
        #Incializar valores
        if motor.getJugadorActivo() == jugador:
            mejorPuntuacion = float('-inf')
        else:
            mejorPuntuacion = float('inf')

        movimientos = motor.posiblesMovimientos()

        if (len(movimientos) > 0):
            pos = random.randint(0, len(movimientos)-1)
            mejorMovimiento = movimientos[pos]
        else:
            mejorMovimiento = None

        for movimiento in movimientos:
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