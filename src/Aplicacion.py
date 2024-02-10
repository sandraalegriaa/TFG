import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import Constantes as c
from interfaces import MenuPrincipal

class Aplicacion: 

    def __init__(self):
        self._menuPrincipal = MenuPrincipal()

    def lanzaJuego(self):
        self._menuPrincipal.iniciaMenu()

def main():
    app = Aplicacion()
    app.lanzaJuego()

if __name__ == "__main__":
    main()