import sys
from os.path import dirname
sys.path.append(dirname(__file__))
import time
import Constantes as c
from motores import MotorDeJuego
from jugadores import JugadorInteligente


def juegaUnaPartida(jugador1:JugadorInteligente,jugador2:JugadorInteligente,juego: MotorDeJuego):
        
        i = 0
        tiempos_jugador1 = []
        tiempos_jugador2 = []

        while (not juego.comprobarFinJuego()):

            i+= 1
            
            if (not juego.comprobarPosiblesMovimientos()):

                #Cambiar el turno al siguiente jugador
                juego.cambiarTurno(juego.getJugadorActivo())
            else:
                inicio_tiempo = time.time()
                if (juego.getJugadorActivo() == jugador1):
                    movimiento = jugador1.eligeMovimientoTablaTrasposicion(juego)
                    tiempos_jugador1.append(time.time() - inicio_tiempo)
                else:
                    movimiento = jugador2.eligeMovimientoTablaTrasposicion(juego)
                    tiempos_jugador2.append(time.time() - inicio_tiempo)

                if movimiento is not None:
                    fila = movimiento[0]
                    columna = movimiento[1]

                    #Comprobar si hay fichas que han quedado encerradas tras el movimiento
                    celdas = juego.fichasContrariasEncerradas(fila,columna)

                    #Realizar el movimiento
                    print("MOVIMIENTO: ", i)
                    juego.colocarFicha(fila,columna,celdas)   

        ganador = juego.comprobarGanador()
        print(f"Ganador: {ganador}")

        # Calcular e imprimir la media de tiempo por movimiento de cada jugador
        media_tiempo_jugador1 = sum(tiempos_jugador1) / len(tiempos_jugador1) if tiempos_jugador1 else 0
        media_tiempo_jugador2 = sum(tiempos_jugador2) / len(tiempos_jugador2) if tiempos_jugador2 else 0

        # Retornar el ganador y los tiempos medios de cada jugador
        return ganador, media_tiempo_jugador1, media_tiempo_jugador2

def main():
    
    contadorNegras = 0
    contadorBlancas = 0
    contadorEmpates = 0

    tiempos_jugador1_total = []
    tiempos_jugador2_total = []

    for partida in range(c.PARTIDAS):  

        print("JUGANDO PARTIDA...", partida)
        
        jugador1 = JugadorInteligente(c.NEGRO,c.P1,c.EVALUADOR_COMBINADO)
        jugador2 = JugadorInteligente(c.BLANCO,c.P2,c.EVALUADOR_RANDOM)

        juego = MotorDeJuego(jugador1,jugador2)

        # Asegúrate de que juegaUnaPartida ahora retorne también los tiempos medios
        ganador, tiempo_medio_jugador1, tiempo_medio_jugador2 = juegaUnaPartida(jugador1, jugador2, juego)

        tiempos_jugador1_total.append(tiempo_medio_jugador1)
        tiempos_jugador2_total.append(tiempo_medio_jugador2)

        if ganador == c.JUGADOR1_GANA:
            contadorNegras += 1
        elif ganador == c.JUGADOR2_GANA:
            contadorBlancas += 1
        else:
            contadorEmpates += 1

        # Imprimir estadísticas de la partida
        print(f"NEGRAS;BLANCAS;EMPATES: {contadorNegras};{contadorBlancas};{contadorEmpates}")
        print(f"Media de tiempo por movimiento en esta partida - Jugador 1: {tiempo_medio_jugador1:.2f} segundos, Jugador 2: {tiempo_medio_jugador2:.2f} segundos")

    # Calcular la media de tiempo por movimiento de cada jugador en todas las partidas
    media_tiempos_jugador1 = sum(tiempos_jugador1_total) / len(tiempos_jugador1_total)
    media_tiempos_jugador2 = sum(tiempos_jugador2_total) / len(tiempos_jugador2_total)

    # Imprimir la media de tiempo por movimiento de cada jugador en todas las partidas
    print(f"Media de tiempo por movimiento de todas las partidas - Jugador 1: {media_tiempos_jugador1:.2f} segundos, Jugador 2: {media_tiempos_jugador2:.2f} segundos")

if __name__ == "__main__":
    main()