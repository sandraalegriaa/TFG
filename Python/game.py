#Juego Othello
import pygame as pg
import sys
import math

#Constantes

#Dimensiones
VENTANA_LARGO = 700
VENTANA_ANCHO = 700

ORIGEN_TABLERO = {'x':117,'y':117}
FIN_TABLERO = {'x':583,'y':583}
DIM_TABLERO = FIN_TABLERO['x']-ORIGEN_TABLERO['x']
CELDAS = 8
DIM_CELDA = DIM_TABLERO / CELDAS
DIM_FICHA = DIM_CELDA

#Imagenes
IMG_TABLERO = "./Assets/Board-othello.png"
IMG_FICHA_BLANCA = "./Assets/Pieza-blanca.png"
IMG_FICHA_NEGRA = "./Assets/Pieza-negra.png"

#Colores RGB
BLANCO = (255,255,255)
NEGRO = (0,0,0)

#Jugadores
P1 = 1
P2 = 2

#Tablero (hacer con un enumerado)
A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6 
H = 7

def main():
    App = Aplicacion()
            
class Aplicacion:

    def __init__(self):

        pg.init()

        #Crear tablero de juego
        self.tablero = [[0 for i in range(CELDAS)] for j in range(CELDAS)]

        self.jugadorActivo = P1

        #Configurar ventana de juego
        self.ventana = pg.display.set_mode((VENTANA_ANCHO, VENTANA_LARGO))
        pg.display.set_caption("Othello")
        self.ventana.fill(BLANCO)

        self.asset_tablero, self.asset_blanca, self.asset_negra, self.asset_blanca_trans, self.asset_negra_trans = self.cargarImagenes()

        self.inicializarTablero()

        #Actualizar ventana
        pg.display.update()

        while True:
            self.gestionEventos()
            self.posicionRaton()
       
    def gestionEventos(self):

        for event in pg.event.get():
            #Cerrar ventana
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            #Click del raton
            elif event.type == pg.MOUSEBUTTONDOWN:
                #Coordenadas del click
                pos = pg.mouse.get_pos()
                if (pos != None):
                    #Obtener celda
                    fila, columna = self.obtenerCelda(pos)
                    
                    #Colocacion de las fichas
                    if (self.dentroCeldas(fila,columna) and self.tablero[fila][columna] == 0):
                        
                        if (self.adyacencia(fila,columna)):
                            #Indicar que jugador coloca la ficha en la matriz
                            if (self.jugadorActivo == P1):
                                self.tablero[fila][columna] = 1
                            else: 
                                self.tablero[fila][columna] = 2

                            #Colocar ficha del jugador
                            ficha = self.obtenerFichaJugador()
                            self.colocarFicha(ficha,fila,columna)       

                            #BORRAR AL ACABAR
                            print(self.tablero)
                            print(f"Columna: {columna}, fila: {fila}")
                         
    def adyacencia (self,fila,columna):

        condp2 = False
        condp1 = False

        adyacente = False

        #Borde superior del tablero
        if (not ((fila-1) < 0)):
            condp2 = self.tablero[fila-1][columna] == P2
            condp1 = self.tablero[fila-1][columna] == P1
            #Esquina superior izquierda
            if (not ((columna - 1) < 0)):
                condp2 = condp2 or self.tablero[fila-1][columna-1] == P2
                condp1 = condp1 or self.tablero[fila-1][columna-1] == P1
            #Esquina superior izquierda
            if (not ((columna + 1) >= CELDAS)):
                condp2 = condp2 or self.tablero[fila-1][columna+1] == P2
                condp1 = condp1 or self.tablero[fila-1][columna+1] == P1
        
        #Borde inferior del tablero
        if (not ((fila + 1) >= CELDAS)):
            condp2 = condp2 or self.tablero[fila+1][columna] == P2 
            condp1 = condp1 or self.tablero[fila+1][columna] == P1 
            #Esquina inferior izquierda
            if (not ((columna - 1) < 0)):
                condp2 = condp2 or self.tablero[fila+1][columna-1] == P2
                condp1 = condp1 or self.tablero[fila+1][columna-1] == P1
            #Esquina inferior derecha
            if (not ((columna + 1) >= CELDAS)):
                condp2 = condp2 or self.tablero[fila+1][columna+1] == P2
                condp1 = condp1 or self.tablero[fila+1][columna+1] == P1

        #Borde izquierdo del tablero
        if (not ((columna - 1) < 0)):
            condp2 = condp2 or self.tablero[fila][columna-1] == P2
            condp1 = condp1 or self.tablero[fila][columna-1] == P1
        #Borde derecho del tablero
        if (not ((columna + 1) >= CELDAS)):
            condp2 = condp2 or self.tablero[fila][columna+1] == P2
            condp1 = condp1 or self.tablero[fila][columna+1] == P1

        if (self.jugadorActivo == P1 and condp2):
            adyacente = True
        elif (self.jugadorActivo == P2 and condp1):
            adyacente = True

        return adyacente
                       
    def colocarFicha(self,ficha,fila,columna):
        self.ventana.blit(ficha, (ORIGEN_TABLERO['x'] + columna * DIM_CELDA,ORIGEN_TABLERO['y'] + fila * DIM_CELDA))
        pg.display.update()

    def obtenerFichaJugador(self):

        if (self.jugadorActivo == P1):
            ficha = self.asset_negra
            self.jugadorActivo = P2
        else:
            ficha = self.asset_blanca
            self.jugadorActivo = P1
    
        return ficha

    def obtenerCelda(self, pos):

        fila = math.floor(((pos[1] - ORIGEN_TABLERO['y']) / DIM_CELDA))
        columna = math.floor(((pos[0] - ORIGEN_TABLERO['x']) / DIM_CELDA))

        return fila,columna

    def dentroCeldas(self, fila,columna):

        return fila in range(0,8) and columna in range(0,8)

    
    def dentroTablero(self, coord):

        return (coord[0] in range(ORIGEN_TABLERO['x'], FIN_TABLERO['x']) and coord[1] in range(ORIGEN_TABLERO['y'], FIN_TABLERO['y']))
    
    def cargarImagenes(self):

        asset_tablero = self.imagen(IMG_TABLERO,VENTANA_ANCHO)

        asset_blanca = self.imagen(IMG_FICHA_BLANCA,DIM_FICHA)
        
        asset_negra = self.imagen(IMG_FICHA_NEGRA, DIM_FICHA)

        asset_blanca_trans = self.imagen(IMG_FICHA_BLANCA,DIM_FICHA)

        asset_negra_trans = self.imagen(IMG_FICHA_NEGRA,DIM_FICHA)

        return asset_tablero, asset_blanca, asset_negra, asset_blanca_trans, asset_negra_trans
    
    def imagen(self,ruta,dim):
    
        try:
            asset = pg.image.load(ruta)
            asset = pg.transform.scale(asset, (dim,dim))
        except FileNotFoundError as enf:
            print(f"No se pudo encontrar la imagen {ruta}")
            raise SystemExit(enf)
        except pg.error as er:
            print(f"No se pudo abrir la imagen {ruta}")
            raise SystemExit(er)
        
        return asset

    def inicializarTablero (self):

        #Tablero
        self.ventana.blit(self.asset_tablero, (0,0))

        #Fichas blancas
        self.ventana.blit(self.asset_blanca, (ORIGEN_TABLERO['x'] + 3 * DIM_CELDA,ORIGEN_TABLERO['y'] + D * DIM_CELDA))
        self.tablero[3][D] = 2
        self.ventana.blit(self.asset_blanca, (ORIGEN_TABLERO['x'] + 4 * DIM_CELDA,ORIGEN_TABLERO['y'] + E * DIM_CELDA))
        self.tablero[4][E] = 2

        #Fichas negras
        self.ventana.blit(self.asset_negra, (ORIGEN_TABLERO['x'] + 4 * DIM_CELDA,ORIGEN_TABLERO['y'] + D * DIM_CELDA))
        self.tablero[4][D] = 1
        self.ventana.blit(self.asset_negra, (ORIGEN_TABLERO['x'] + 3 * DIM_CELDA,ORIGEN_TABLERO['y'] + E * DIM_CELDA))
        self.tablero[3][E] = 1

    def posicionRaton (self):

        posRaton = pg.mouse.get_pos()

        if (self.dentroTablero(posRaton)):

            fila, columna = self.obtenerCelda(posRaton)
            #Colocar ficha del jugador
            #ficha = self.obtenerFichaJugador()
            #pg.mouse.set_visible(False)
            #self.colocarFicha(ficha,fila,columna)
            
        else: 
            pg.mouse.set_visible(True)
            pg.mouse.set_cursor()


if __name__ == "__main__":

    main()