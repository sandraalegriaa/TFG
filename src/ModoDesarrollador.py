import sys
import os
from os.path import dirname
sys.path.append(dirname(__file__))
import time
import Constantes as c
from motores import MotorDeJuego
from jugadores import JugadorInteligente
import datetime


def juegaUnaPartida(jugador1:JugadorInteligente,jugador2:JugadorInteligente,juego: MotorDeJuego):
        
        t1 = 0
        t2 = 0
        i = 0
        tiempos_jugador1 = []
        tiempos_jugador2 = []

        while (not juego.comprobarFinJuego()): 
            if (not juego.comprobarPosiblesMovimientos()):

                #Cambiar el turno al siguiente jugador
                juego.cambiarTurno(juego.getJugadorActivo())
            else:
                i+= 1
                inicio_tiempo = time.time()
                if (juego.getJugadorActivo() == jugador1):
                    movimiento = jugador1.eligeMovimiento(juego)
                    t1 = time.time() - inicio_tiempo
                    tiempos_jugador1.append(t1)
                else:
                    movimiento = jugador2.eligeMovimiento(juego)
                    t2 = time.time() - inicio_tiempo
                    tiempos_jugador2.append(t2)

                if movimiento is not None:
                    fila = movimiento[0]
                    columna = movimiento[1]

                    #Comprobar si hay fichas que han quedado encerradas tras el movimiento
                    celdas = juego.fichasContrariasEncerradas(fila,columna)

                    #Realizar el movimiento
                    print("MOVIMIENTO: ", i)

                    juego.colocarFicha(fila,columna,celdas)  

                    print(t1,t2)
                    t1 = 0
                    t2 = 0 

        print(juego._tablero)
        ganador = juego.comprobarGanador()
        print(f"Ganador: {ganador}")

        # Calcular e imprimir la media de tiempo por movimiento de cada jugador
        media_tiempo_jugador1 = sum(tiempos_jugador1) / len(tiempos_jugador1) if tiempos_jugador1 else 0
        media_tiempo_jugador2 = sum(tiempos_jugador2) / len(tiempos_jugador2) if tiempos_jugador2 else 0

        # Retornar el ganador y los tiempos medios de cada jugador
        return ganador, media_tiempo_jugador1, media_tiempo_jugador2

def main():
    
    #Obtener tiempo actual
    ahora = datetime.datetime.now()

    contadorNegras = 0
    contadorBlancas = 0
    contadorEmpates = 0

    tiempos_jugador1_total = []
    tiempos_jugador2_total = []

    #Archivo con nombre fecha y hora actual
    archivo  = ahora.strftime("%Y-%m-%d_%H-%M-%S") + '.txt'

    #Ruta al directorio que almacena los datos
    rutaDirectorio = os.path.join('..', 'Datos')

    #Comprobar que el directorio Datos exista
    if not os.path.exists(rutaDirectorio):
        os.makedirs(rutaDirectorio)

    #Ruta del fichero
    rutaCompleta = os.path.join(rutaDirectorio, archivo)

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

        with open(rutaCompleta, 'a') as a:
            a.write(f"Partida:{partida}\n")
            a.write(f"NEGRAS;BLANCAS;EMPATES: {contadorNegras};{contadorBlancas};{contadorEmpates}\n")
            a.write(f"Media de tiempo por movimiento en esta partida - Jugador 1: {tiempo_medio_jugador1:.2f} segundos, Jugador 2: {tiempo_medio_jugador2:.2f} segundos\n")

        # Imprimir estadísticas de la partida
        print(f"NEGRAS;BLANCAS;EMPATES: {contadorNegras};{contadorBlancas};{contadorEmpates}")
        print(f"Media de tiempo por movimiento en esta partida - Jugador 1: {tiempo_medio_jugador1:.2f} segundos, Jugador 2: {tiempo_medio_jugador2:.2f} segundos")

    # Calcular la media de tiempo por movimiento de cada jugador en todas las partidas
    media_tiempos_jugador1 = sum(tiempos_jugador1_total) / len(tiempos_jugador1_total)
    media_tiempos_jugador2 = sum(tiempos_jugador2_total) / len(tiempos_jugador2_total)

    # Imprimir la media de tiempo por movimiento de cada jugador en todas las partidas
    print(f"Media de tiempo por movimiento de todas las partidas - Jugador 1: {media_tiempos_jugador1:.2f} segundos, Jugador 2: {media_tiempos_jugador2:.2f} segundos")
    with open(rutaCompleta, 'a') as a:
            a.write(f"Media de tiempo por movimiento de todas las partidas - Jugador 1: {media_tiempos_jugador1:.2f} segundos, Jugador 2: {media_tiempos_jugador2:.2f} segundos")

if __name__ == "__main__":
    main()