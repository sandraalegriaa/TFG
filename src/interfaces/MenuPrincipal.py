from dataclasses import dataclass

import Constantes as c
import pygame as pg
import sys
import math as m

from motores import IMotorDeJuego
from motores import MotorDeJuego
from interfaces import InterfazOthello
from jugadores import JugadorHumano
from jugadores import IJugador

@dataclass
class MenuPrincipal ():

    _juego : IMotorDeJuego
    _interfazOthello: InterfazOthello
    _jugador1: IJugador
    _jugador2: IJugador

    _assetFondoMenu: pg.image

    _fuente: pg.font

    """
    _assetBotonJugadorJugador: pg.image
    _assetBotonJugadorIA: pg.image
    _assetBotonJugadorJugadorEncima: pg.image
    _assetBotonJugadorIAEncima: pg.image
    """ 
    def __init__(self):

        #Iniciar pygame
        pg.init()

        #Configurar ventana de juego
        self._ventana = self.configurarVentana()

        #Cargar assets de la interfaz
        self._assetFondoMenu, self._assetBotonJugadorJugador, self._assetBotonJugadorJugadorEncima, self._assetBotonJugadorIA, self._assetBotonJugadorIAEncima = self.cargarImagenes()

        #Cargar fuente
        self._fuente = pg.font.Font(c.FUENTE, 30) 

        #Definir botones 
        self._botonJugadorJugador = pg.Rect(((c.VENTANA_ANCHO // 2) - c.ANCHURA_BOTON // 2), ((c.VENTANA_LARGO // 2) - (c.ALTURA_BOTON//2)) - 70, c.ANCHURA_BOTON, c.ALTURA_BOTON)
        self._botonJugadorIA = pg.Rect(((c.VENTANA_ANCHO // 2) - c.ANCHURA_BOTON // 2), ((c.VENTANA_LARGO // 2) - (c.ALTURA_BOTON//2)) + 70, c.ANCHURA_BOTON, c.ALTURA_BOTON)
        
        self._assetBotonJugadores = self._assetBotonJugadorJugador
        self._assetBotonIA = self._assetBotonJugadorIA

        self.inicializarInterfaz()

        #Crear los botones en la interfaz
        self.dibujaBoton(self._botonJugadorJugador,self._assetBotonJugadorJugador, c.TEXTO_BOTON_JUGADORES)
        self.dibujaBoton(self._botonJugadorIA,self._assetBotonJugadorIA, c.TEXTO_BOTON_IA)

        #Actualizar ventana
        pg.display.update()

    def configurarVentana(self):
        """Configurar la ventana de la aplicación"""

        ventana = pg.display.set_mode((c.VENTANA_ANCHO, c.VENTANA_LARGO))
        pg.display.set_caption(c.TITULO_INTERFAZ)
        ventana.fill(c.MARRON_RGB)

        return ventana
    
    def inicializarInterfaz(self):
        """Inicializar menu principal"""

        #Tablero
        self._ventana.blit(self._assetFondoMenu, (0,0))

        #Actualizar ventana
        pg.display.update()
    
    def imagen(self,ruta,dimX,dimY):
        """Obtener imagen de un asset"""
    
        try:
            asset = pg.image.load(ruta)
            asset = pg.transform.scale(asset, (dimX,dimY))
        except FileNotFoundError as enf:
            print(f"No se pudo encontrar la imagen {ruta}")
            raise SystemExit(enf)
        except pg.error as er:
            print(f"No se pudo abrir la imagen {ruta}")
            raise SystemExit(er)
        
        return asset
    
    def cargarImagenes(self):
        """Cargar assets"""

        asset_fondo = self.imagen(c.IMG_FONDO_MENU_PRINCIPAL,c.VENTANA_ANCHO,c.VENTANA_LARGO)

        #TODO: Cambiar a assets correctos
        assetBotonJugadorJugador = self.imagen(c.IMG_BOTON,c.ANCHURA_BOTON,c.ALTURA_BOTON)
        assetBotonJugadorJugadorEncima = self.imagen(c.IMG_BOTON_ENCIMA,c.ANCHURA_BOTON,c.ALTURA_BOTON)
        assetBotonJugadorIA = self.imagen(c.IMG_BOTON,c.ANCHURA_BOTON,c.ALTURA_BOTON)
        assetBotonJugadorIAEncima = self.imagen(c.IMG_BOTON_ENCIMA,c.ANCHURA_BOTON,c.ALTURA_BOTON)

        return asset_fondo, assetBotonJugadorJugador, assetBotonJugadorJugadorEncima, assetBotonJugadorIA, assetBotonJugadorIAEncima
    
    def dibujaBoton(self,boton: pg.rect,asset: pg.image, texto: str): 
        """Crea el boton en la interfaz"""  
        self._ventana.blit(asset, boton.topleft)
        textoBoton = self._fuente.render(texto, True, (255, 255, 255))
        dimensionesTexto = self._fuente.size(texto)
        anchoTexto = dimensionesTexto[0]
        alturaTexto = dimensionesTexto[1]
        self._ventana.blit(textoBoton, (boton.x + c.ANCHURA_BOTON//2 - (anchoTexto//2), boton.y + c.ALTURA_BOTON//2-(alturaTexto//1.5)))
        

    def gestionEventos(self):
        """Gestionar eventos en el menu principal"""
        for event in pg.event.get():
            #Cerrar ventana
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self._botonJugadorJugador.collidepoint(event.pos):
                    #Crear dos jugadores humanos
                    self._jugador1 = JugadorHumano(c.NEGRO,c.P1)
                    self._jugador2 = JugadorHumano(c.BLANCO,c.P2)
                    self._juego = MotorDeJuego(self._jugador1, self._jugador2)
                    self._interfazOthello = InterfazOthello()
                    self._juego.juega(self._interfazOthello)
                    print("Botón Jugador vs Jugador presionado")
                    pg.quit()
                elif self._botonJugadorIA.collidepoint(event.pos):
                    print("Botón 2 presionado")
        
        #Detectar ratón sobre botones           
        posicion = pg.mouse.get_pos()

        antiguoAsset = self._assetBotonJugadores
        #Boton jugador vs jugador
        if self._botonJugadorJugador.collidepoint(posicion):
            self._assetBotonJugadores = self._assetBotonJugadorJugadorEncima
        else: 
            self._assetBotonJugadores = self._assetBotonJugadorJugador

        #Comprobar si la situación ha cambiado 
        if self._assetBotonJugadores != antiguoAsset:
            redibujarBotonJugadores = True
        else: 
            redibujarBotonJugadores = False

        #Boton jugador vs IA
        antiguoAsset = self._assetBotonIA

        if self._botonJugadorIA.collidepoint(posicion):
            self._assetBotonIA = self._assetBotonJugadorIAEncima
        else: 
            self._assetBotonIA = self._assetBotonJugadorIA

        #Comprobar si la situación ha cambiado 
        if self._assetBotonIA != antiguoAsset:
            redibujarBotonIA = True
        else: 
            redibujarBotonIA = False

        if redibujarBotonJugadores:
            self.dibujaBoton(self._botonJugadorJugador,self._assetBotonJugadores, c.TEXTO_BOTON_JUGADORES)
            #Actualizar ventana
            pg.display.update()
        
        if redibujarBotonIA:
            self.dibujaBoton(self._botonJugadorIA,self._assetBotonIA, c.TEXTO_BOTON_IA)
            #Actualizar ventana
            pg.display.update()
    
    def iniciaMenu(self):

        while(True):
            self.gestionEventos()