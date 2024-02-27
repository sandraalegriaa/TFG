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
            
            print("MOVIMIENTO: ", i)
            
            if (not self._juego.comprobarPosiblesMovimientos()):
                print("NO PUEDE COLOCAR, CAMBIAR TURNO AL SIGUIENTE")

                #Cambiar el turno al siguiente jugador
                self._juego.cambiarTurno(self._juego.getJugadorActivo())
            else:
                if (self._juego.getJugadorActivo() == self._jugador1):

                    movimiento = self._jugador1.eligeMovimiento(self._juego)
                else:
                    movimiento = self._jugador2.eligeMovimiento(self._juego)

                fila = movimiento[0]
                columna = movimiento[1]

                print("JUEGA EL JUGADOR", self._juego.getJugadorActivo().getTurno())

                #Comprobar si hay fichas que han quedado encerradas tras el movimiento
                celdas = self._juego.fichasContrariasEncerradas(fila,columna)

                #Realizar el movimiento
                self._juego.colocarFicha(fila,columna,celdas)  

                

                print(self._juego.getTablero())

        ganador = self._juego.comprobarGanador()

        print(ganador)

def main():
    desarrollador = ModoDesarrollador()
    desarrollador.juegaUnaPartida()

if __name__ == "__main__":
    main()