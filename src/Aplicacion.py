import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from interfaces import Interfaz
from motores import MotorDeJuego
from jugadores import JugadorHumano

class Aplicacion: 

    def __init__(self):
    
        self._interfaz = Interfaz()        
        self._jugador1 = JugadorHumano(1,1)
        self._jugador2 = JugadorHumano(2,2)
        self._juego = MotorDeJuego(self._jugador1, self._jugador2)

    def lanzaJuego(self):

        self._juego.juega(self._interfaz)

def main():

    app = Aplicacion()
    app.lanzaJuego()
    

if __name__ == "__main__":
    print(sys.path)
    main()