import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import Constantes as c
from interfaces import Interfaz
from motores import MotorDeJuego
from jugadores import JugadorHumano

class Aplicacion: 

    def __init__(self):
        self._interfaz = Interfaz()        
        self._jugador1 = JugadorHumano(c.NEGRO,c.P1)
        self._jugador2 = JugadorHumano(c.BLANCO,c.P2)
        self._juego = MotorDeJuego(self._jugador1, self._jugador2)

    def lanzaJuego(self):
        self._juego.juega(self._interfaz)

def main():
    app = Aplicacion()
    app.lanzaJuego()

if __name__ == "__main__":
    main()