import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import Constantes as c
from motores import IMotorDeJuego
from motores import MotorDeJuego
from jugadores import JugadorInteligente

class ModoDesarrollador: 

    _juego : IMotorDeJuego
    _jugador1: JugadorInteligente
    _jugador2: JugadorInteligente

    def __init__(self):
        self._jugador1 = JugadorInteligente(c.NEGRO,c.P1,c.EVALUADOR_RANDOM)
        self._jugador2 = JugadorInteligente(c.BLANCO,c.P2,c.EVALUADOR_RANDOM)
        self._juego = MotorDeJuego(self._jugador1,self._jugador2)

    def juegaUnaPartida(self):
        i = 0

        while (not self._juego.comprobarFinJuego()):

            i+= 1
            
            if (not self._juego.comprobarPosiblesMovimientos()):
                #Cambiar el turno al siguiente jugador
                self._juego.cambiarTurno(self._juego.getJugadorActivo())
            else:

                if (self._juego.getJugadorActivo() == self._jugador1):
                    movimiento = self._jugador1.eligeMovimiento(self._juego)
                else:
                    movimiento = self._jugador2.eligeMovimiento(self._juego)

                if movimiento is not None:
                    fila = movimiento[0]
                    columna = movimiento[1]

                    #Comprobar si hay fichas que han quedado encerradas tras el movimiento
                    celdas = self._juego.fichasContrariasEncerradas(fila,columna)

                    #Realizar el movimiento
                    self._juego.colocarFicha(fila,columna,celdas)              


        ganador = self._juego.comprobarGanador()
        
        print("MOVIMIENTO: ", i)

        print(self._juego.getTablero())   

        print(ganador)

        return ganador

def juegaUnaPartidaFuera(jugador1,jugador2,juego):
        i = 0

        while (not juego.comprobarFinJuego()):

            i+= 1
            
            if (not juego.comprobarPosiblesMovimientos()):

                #Cambiar el turno al siguiente jugador
                juego.cambiarTurno(juego.getJugadorActivo())
            else:

                if (juego.getJugadorActivo() == jugador1):
                    movimiento = jugador1.eligeMovimiento(juego)
                else:
                    movimiento = jugador2.eligeMovimiento(juego)

                if movimiento is not None:
                    fila = movimiento[0]
                    columna = movimiento[1]

                    #Comprobar si hay fichas que han quedado encerradas tras el movimiento
                    celdas = juego.fichasContrariasEncerradas(fila,columna)

                    #Realizar el movimiento
                    juego.colocarFicha(fila,columna,celdas)          

        ganador = juego.comprobarGanador()
        
        """print("MOVIMIENTO: ", i)

        print(juego.getTablero())   

        print(ganador)"""

        return ganador

def main():
    
    contadorNegras = 0
    contadorBlancas = 0
    contadorEmpates = 0

    jugador1 = JugadorInteligente(c.NEGRO,c.P1,c.EVALUADOR_FICHAS)
    jugador2 = JugadorInteligente(c.BLANCO,c.P2,c.EVALUADOR_RANDOM)

    for _ in range(c.PARTIDAS):  

        juego = MotorDeJuego(jugador1,jugador2)

        ganador = juegaUnaPartidaFuera(jugador1,jugador2,juego)

        if ganador == c.JUGADOR1_GANA:
            contadorNegras += 1
        elif ganador == c.JUGADOR2_GANA:
            contadorBlancas += 1
        else:
            contadorEmpates += 1
    
    print("NEGRAS;BLANCAS;EMPATES")
    print(contadorNegras,contadorBlancas,contadorEmpates)

if __name__ == "__main__":
    main()