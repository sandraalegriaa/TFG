from dataclasses import dataclass

import Constantes as c
import pygame as pg
import sys
import math as m

@dataclass
class Interfaz ():

    _asset_tablero: pg.image
    _asset_blanca: pg.image
    _asset_negra: pg.image
    _asset_blanca_trans: pg.image
    _asset_negra_trans: pg.image

    def __init__(self):

        #Iniciar pygame
        pg.init()

        #Configurar ventana de juego
        self._ventana = self.configurarVentana()

        #Cargar assets de la interfaz
        self._asset_tablero, self._asset_blanca, self._asset_negra, self._asset_blanca_trans, self._asset_negra_trans = self.cargarImagenes()

    def configurarVentana(self):
        """Configurar la ventana de la aplicación"""

        ventana = pg.display.set_mode((c.VENTANA_ANCHO, c.VENTANA_LARGO))
        pg.display.set_caption(c.TITULO_INTERFAZ)
        ventana.fill(c.BLANCO_RGB)

        return ventana

    def inicializarInterfaz(self):
        """Inicializar interfaz según las reglas del juego"""

        #Tablero
        self._ventana.blit(self._asset_tablero, (0,0))

        #Fichas blancas 
        self._ventana.blit(self._asset_blanca, self.deCeldaAPixel(3,c.D))
        self._ventana.blit(self._asset_blanca, self.deCeldaAPixel(4,c.E))

        #Fichas negras
        self._ventana.blit(self._asset_negra, self.deCeldaAPixel(4,c.D))
        self._ventana.blit(self._asset_negra, self.deCeldaAPixel(3,c.E))

        #Actualizar ventana
        pg.display.update()


    def cargarImagenes(self):
        """Cargar assets"""

        asset_tablero = self.imagen(c.IMG_TABLERO,c.VENTANA_ANCHO)

        asset_blanca = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA)
        
        asset_negra = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA)

        asset_blanca_trans = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA)

        asset_negra_trans = self.imagen(c.IMG_FICHA_NEGRA,c.DIM_FICHA)

        return asset_tablero, asset_blanca, asset_negra, asset_blanca_trans, asset_negra_trans
    
    def imagen(self,ruta,dim):
        """Obtener imagen de un asset"""
    
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
    
    
    def deCeldaAPixel(self, fila, columna):
        """Transformar una celda en coordenadas (x,y)"""

        x = c.ORIGEN_TABLERO['x'] + columna * c.DIM_CELDA
        y = c.ORIGEN_TABLERO['y'] + fila * c.DIM_CELDA

        return (x,y)
    
    def obtenerCelda(self, pos):
        """Transformar coordenadas (x,y) en una celda del tablero"""

        fila = m.floor(((pos[1] - c.ORIGEN_TABLERO['y']) / c.DIM_CELDA))
        columna = m.floor(((pos[0] - c.ORIGEN_TABLERO['x']) / c.DIM_CELDA))

        return fila,columna

    def gestionEventos(self, motor):
        """Gestionar eventos en la interfaz"""

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
                    if (motor.dentroCeldas(fila,columna) and motor.obtenerValorCelda(fila,columna) == 0):
                        
                        if (self.adyacencia(fila,columna)):
                            #Indicar que jugador coloca la ficha en la matriz
                            motor.modificarValorCelda(fila,columna,self._jugadorActivo.getTurno())

                            #Colocar ficha del jugador
                            ficha = self.obtenerFichaJugador()
                            self.colocarFicha(ficha,fila,columna)       

                            #BORRAR AL ACABAR
                            print(motor.getTablero())
                            print(f"Columna: {columna}, fila: {fila}")
                         

