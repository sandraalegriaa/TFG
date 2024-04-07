import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import Constantes as c
from motores import MotorDeJuego
from jugadores import JugadorInteligente


def juegaUnaPartida(jugador1:JugadorInteligente,jugador2:JugadorInteligente,juego: MotorDeJuego):
        i = 0

        while (not juego.comprobarFinJuego()):

            i+= 1
            
            if (not juego.comprobarPosiblesMovimientos()):

                #Cambiar el turno al siguiente jugador
                juego.cambiarTurno(juego.getJugadorActivo())
            else:

                if (juego.getJugadorActivo() == jugador1):
                    movimiento = jugador1.eligeMovimientoTablaTrasposicion(juego)
                else:
                    movimiento = jugador2.eligeMovimientoTablaTrasposicion(juego)

                if movimiento is not None:
                    fila = movimiento[0]
                    columna = movimiento[1]

                    #Comprobar si hay fichas que han quedado encerradas tras el movimiento
                    celdas = juego.fichasContrariasEncerradas(fila,columna)

                    #Realizar el movimiento
                    print("MOVIMIENTO: ", i)
                    juego.colocarFicha(fila,columna,celdas)   

        ganador = juego.comprobarGanador()
        
        print("MOVIMIENTO: ", i)

        print(juego.getTablero())   

        print(ganador)

        return ganador

def main():
    
    contadorNegras = 0
    contadorBlancas = 0
    contadorEmpates = 0

    jugador1 = JugadorInteligente(c.NEGRO,c.P1,c.EVALUADOR_COMBINADO)
    jugador2 = JugadorInteligente(c.BLANCO,c.P2,c.EVALUADOR_RANDOM)

    for partida in range(c.PARTIDAS):  

        print("JUGANDO PARTIDA...", partida)

        juego = MotorDeJuego(jugador1,jugador2)

        ganador = juegaUnaPartida(jugador1,jugador2,juego)

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