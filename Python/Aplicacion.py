import Constantes as c
from Interfaz import Interfaz
from MotorDeJuego import MotorDeJuego

class Aplicacion: 

    def __init__(self):
    
        self.interfaz = Interfaz()        
        self.juego = MotorDeJuego(self.interfaz)

    def lanzaJuego(self):

        self.juego.juega()

def main():

    app = Aplicacion()
    app.lanzaJuego()
    

if __name__ == "__main__":
    main()