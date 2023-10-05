import math
import Constantes as c

class MotorDeJuego:

    def __init__(self, interfaz, jugador1, jugador2):

        self.tablero = [[0 for i in range(c.CELDAS)] for j in range(c.CELDAS)]

        #Comienzan la colocacion las negras
        self.jugadorActivo = c.P1

        self.interfaz = interfaz

        self.jugador1 = jugador1
        self.jugador2 = jugador2


    def juega(self):

        self.inicializarTablero()

        
        while True:
            
            self.interfaz.gestionEventos()

        return None
    
    def getInterfaz(self):
        return self.interfaz
    
    def getTablero(self):
        return self.tablero
    
    def getJugadorActivo(self):
        return self.jugadorActivo
    
    def setJugadorActivo(self,jugador):
        self.jugadorActivo = jugador
    
    def obtenerCelda(self, pos):

        fila = math.floor(((pos[1] - c.ORIGEN_TABLERO['y']) / c.DIM_CELDA))
        columna = math.floor(((pos[0] - c.ORIGEN_TABLERO['x']) / c.DIM_CELDA))

        return fila,columna
    
    def dentroCeldas(self, fila,columna):

        return fila in range(0,8) and columna in range(0,8)
    
    def inicializarTablero (self):

        #Fichas blancas
        self.tablero[3][c.D] = 2
        self.tablero[4][c.E] = 2

        #Fichas negras
        self.tablero[4][c.D] = 1
        self.tablero[3][c.E] = 1

        self.interfaz.inicializarInterfaz()

                
