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

        #Definir botones 
        _anchura_boton, _altura_boton = 200, 50
        self._botonJugadorJugador = pg.Rect((c.VENTANA_ANCHO - _anchura_boton) // 2, (c.VENTANA_LARGO // 2) - _altura_boton - 40, _anchura_boton, _altura_boton)
        self._botonJugadorIA = pg.Rect((c.VENTANA_ANCHO - _anchura_boton) // 2, (c.VENTANA_LARGO // 2) - _altura_boton + 40, _anchura_boton, _altura_boton)

        self._assetBotonJugadorJugador = c.BLANCO_RGB
        self._assetBotonJugadorJugadorEncima = c.NEGRO_RGB
        self._assetBotonJugadorIA = c.BLANCO_RGB
        self._assetBotonJugadorIAEncima = c.NEGRO_RGB

        self._assetBotonJugadores = self._assetBotonJugadorJugador
        self._assetBotonIA = self._assetBotonJugadorIA

        #Crear los botones en la interfaz
        self.dibujaBoton(self._botonJugadorJugador,self._assetBotonJugadorJugador)
        self.dibujaBoton(self._botonJugadorIA,self._assetBotonJugadorIA)

        #Actualizar ventana
        pg.display.update()

    def configurarVentana(self):
        """Configurar la ventana de la aplicación"""

        ventana = pg.display.set_mode((c.VENTANA_ANCHO, c.VENTANA_LARGO))
        pg.display.set_caption(c.TITULO_INTERFAZ)
        ventana.fill(c.MARRON_RGB)

        return ventana
    
    def dibujaBoton(self,boton: pg.rect ,asset): 
        """Crea el boton en la interfaz"""  
        #TODO : Hacer que funcione con assets personalizados
        pg.draw.rect(self._ventana, asset, boton)

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
            self.dibujaBoton(self._botonJugadorJugador,self._assetBotonJugadores)
            #Actualizar ventana
            pg.display.update()
        
        if redibujarBotonIA:
            self.dibujaBoton(self._botonJugadorIA,self._assetBotonIA)
            #Actualizar ventana
            pg.display.update()
    
    def iniciaMenu(self):

        while(True):
            self.gestionEventos()