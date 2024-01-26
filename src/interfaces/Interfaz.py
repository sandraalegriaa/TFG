from dataclasses import dataclass

import Constantes as c
import pygame as pg
import sys
import math as m

from motores import IMotorDeJuego

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
            
    def colocarFicha(self,ficha,fila,columna):
        """Colocar la ficha en el tablero y actualizar el tablero para que se visualice correctamente"""

        self._ventana.blit(ficha, (c.ORIGEN_TABLERO['x'] + columna * c.DIM_CELDA,c.ORIGEN_TABLERO['y'] + fila * c.DIM_CELDA))
        pg.display.update()

    def obtenerFichaJugador(self, motor : IMotorDeJuego):
        """"Obtener asset de la ficha correspondiente al jugador activo"""

        jugadorActivo = motor.getJugadorActivo()

        if (jugadorActivo.getColor() == c.NEGRO):
            ficha = self._asset_negra
        else:
            ficha = self._asset_blanca
    
        return ficha
    
    def cambiarFichasEncerradas(self, motor: IMotorDeJuego, celdas):
        """Cambiar assets de las fichas encerradas por las fichas del jugador actual"""

        ficha = self.obtenerFichaJugador(motor)

        for [fila,columna] in celdas:
            self.colocarFicha(ficha,fila,columna)


    def gestionEventos(self, motor: IMotorDeJuego):
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
                    print(pos)
                    print()
                    #Colocacion de las fichas
                    if (motor.dentroCeldas(fila,columna) and motor.obtenerValorCelda(fila,columna) == 0):
                        
                        #Comprobar si hay fichas que han quedado encerradas
                        celdas = motor.fichasContrariasEncerradas(fila,columna)

                        if (len(celdas) > 0):

                            #Indicar que jugador coloca la ficha en el tablero
                            motor.modificarValorCelda(fila,columna,motor.getJugadorActivo().getTurno())

                            #Colocar ficha del jugador
                            ficha = self.obtenerFichaJugador(motor)
                            self.colocarFicha(ficha,fila,columna)       

                            motor.cambiarValorFichasEncerradas(celdas)
                            self.cambiarFichasEncerradas(motor, celdas)

                            #Turno del siguiente jugador
                            motor.cambiarTurno(motor.getJugadorActivo())

                            #BORRAR AL ACABAR
                            print(motor.getTablero())
                            print(f"Columna: {columna}, fila: {fila}")
                         

