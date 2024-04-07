from dataclasses import dataclass
from motores import MotorDeJuego
from jugadores.Jugador import Jugador

import Constantes as c
import random


@dataclass
class JugadorInteligente(Jugador):
    """Clase del jugador humano"""

    evaluador : int

    def __init__(self, color, turno,evaluador):
        super().__init__(color,turno)
        self.evaluador = evaluador

    def cambiarEvaluador(self, evaluador:int):
        self.evaluador = evaluador

    #Funciones de evaluación
    def evaluarRandom(self,motor:MotorDeJuego):
        """Evalua el movimiento de manera aleatoria"""

        return random.randint(c.MIN_PUNTUACION, c.MAX_PUNTUACION)
    
    def evaluarFichas(self,motor:MotorDeJuego,jugador:Jugador):
        """Evalua el movimiento en función del número de fichas de los jugadores, cuantas más fichas mejor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        fichasJugador = motor.obtenerFichasJugador(jugador)
        fichasContrario = motor.obtenerFichasJugador(jugadorContrario)

        totalFichas = fichasJugador+fichasContrario

        if (fichasJugador > fichasContrario):
            puntuacion = 100*(fichasJugador/totalFichas)
        elif (fichasJugador < fichasContrario):
            puntuacion = -100*(fichasContrario/totalFichas)
        else:
            puntuacion = 0

        return puntuacion
    
    def evaluarMovilidad(self,motor:MotorDeJuego,jugador:Jugador):
        """Evalua el movimiento en función del número del número de movimientos posibles, cuantos más movimientos mejor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        movimientosJugador = len(motor.posiblesMovimientosJugador(jugador))
        movimientosContrario = len(motor.posiblesMovimientosJugador(jugadorContrario))

        totalMovilidad = movimientosJugador+movimientosContrario

        if (movimientosJugador > movimientosContrario):
            puntuacion = 100*(movimientosJugador/totalMovilidad)
        elif (movimientosJugador < movimientosContrario):
            puntuacion = -100*(movimientosContrario/totalMovilidad)
        else:
            puntuacion = 0

        return puntuacion
    
    def evaluarEsquinas(self,motor:MotorDeJuego,jugador:Jugador):
        """Evalua el movimiento en función del número de esquinas ocupadas con fichas del jugador, cuantas más esquinas mejor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        esquinasJugador = motor.obtenerEsquinasJugador(jugador)
        esquinasContrario = motor.obtenerEsquinasJugador(jugadorContrario)

        puntuacion = 25*esquinasJugador-25*esquinasContrario

        return puntuacion
    
    def evaluarAdyacentes(self,motor:MotorDeJuego,jugador:Jugador):
        """Evalua el movimiento en función del número de fuchas adyacentes a esquinas vacías, cuantas más peor"""

        jugadorContrario = motor.obtenerJugadorContario(jugador)

        adyacentesJugador = motor.obtenerAdyacentesEsquinasJugador(jugador)
        adyacentesContrario = motor.obtenerAdyacentesEsquinasJugador(jugadorContrario)

        puntuacion = -12.5*adyacentesJugador+12.5*adyacentesContrario

        return puntuacion

    def evaluarCombinado(self, motor:MotorDeJuego, jugador:Jugador):
        """Evalúa combinando el número de fichas, la movilidad y las esquinas ocupadas,dando el mismo peso a cada evaluación."""
        
        fichas = self.evaluarFichas(motor, jugador)
        esquinas = self.evaluarEsquinas(motor,jugador)
        adyacentes = self.evaluarAdyacentes(motor,jugador)
        movilidad = self.evaluarMovilidad(motor,jugador)
     
        puntuacion = fichas+esquinas+adyacentes+movilidad     
        
        return puntuacion
    
    def evaluarPesoCasillas(self, motor:MotorDeJuego, jugador:Jugador):
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

    def eligeMovimiento(self,motor:MotorDeJuego):
        puntuacion, movimiento = self.minimax(motor,self,c.MAXIMA_PROFUNDIDAD_MINIMAX)
        return movimiento

    #Minimax
    def minimax(self, motor:MotorDeJuego, jugador: Jugador, profundidad:int, alfa=float('-inf'), beta=float('inf')):
    
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
    
    #Minimax con tabla de trasposicion
    def minimaxTablaTrasposicion(self, motor:MotorDeJuego, jugador: Jugador, profundidad:int, alfa=float('-inf'), beta=float('inf')):
    
        #Comprobar fin de la recursión
        if profundidad == 0 or motor.comprobarFinJuego():
            if (self.evaluador == c.EVALUADOR_RANDOM):
                return self.evaluarRandom(motor), None
            elif (self.evaluador == c.EVALUADOR_COMBINADO):
                return self.evaluarCombinado(motor,jugador), None
                        
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
    