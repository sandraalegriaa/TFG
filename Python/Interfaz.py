import Constantes as c
import pygame as pg
import sys

class Interfaz ():

    def __init__(self):

        pg.init()

        #Configurar ventana de juego
        self.ventana = self.configurarVentana()

        self.asset_tablero, self.asset_blanca, self.asset_negra, self.asset_blanca_trans, self.asset_negra_trans = self.cargarImagenes()

    def configurarVentana(self):

        ventana = pg.display.set_mode((c.VENTANA_ANCHO, c.VENTANA_LARGO))
        pg.display.set_caption(c.TITULO_INTERFAZ)
        ventana.fill(c.BLANCO)

        return ventana

    def inicializarInterfaz(self):

        #Tablero
        self.ventana.blit(self.asset_tablero, (0,0))

        #Fichas blancas 
        self.ventana.blit(self.asset_blanca, self.deCeldaAPixel(3,c.D))
        self.ventana.blit(self.asset_blanca, self.deCeldaAPixel(4,c.E))

        #Fichas negras
        self.ventana.blit(self.asset_negra, self.deCeldaAPixel(4,c.D))
        self.ventana.blit(self.asset_negra, self.deCeldaAPixel(3,c.E))

        #Actualizar ventana
        pg.display.update()

    def deCeldaAPixel(self, fila, columna):

        x = c.ORIGEN_TABLERO['x'] + columna * c.DIM_CELDA
        y = c.ORIGEN_TABLERO['y'] + fila * c.DIM_CELDA

        return (x,y)

    def cargarImagenes(self):

        asset_tablero = self.imagen(c.IMG_TABLERO,c.VENTANA_ANCHO)

        asset_blanca = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA)
        
        asset_negra = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA)

        asset_blanca_trans = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA)

        asset_negra_trans = self.imagen(c.IMG_FICHA_NEGRA,c.DIM_FICHA)

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
    
    def gestionEventos(self):

        for event in pg.event.get():
            #Cerrar ventana
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
