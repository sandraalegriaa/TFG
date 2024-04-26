from dataclasses import dataclass

import Constantes as c
import pygame as pg
import sys
import math as m
import tkinter as tk
from tkinter import filedialog
import os
from typing import Optional
from motores import MotorDeJuego
from Sprites import Ficha
from Sprites import FichaSemiTransparente

@dataclass
class InterfazOthello ():

    #Motor
    _motor : MotorDeJuego

    #Sprites
    _grupoSpritesFichas : pg.sprite.Group
    _nuevaFicha: pg.sprite.Group

    _grupoSpritesFichasSemitransparente : pg.sprite.Group
    _nuevaFichasSemitransparente : pg.sprite.Group

    _angituaFichaSemitransparente : Optional[tuple[int,int]]

    #Assets
    _asset_tablero: pg.Surface
    _asset_fondo: pg.Surface
    _asset_blanca_turno: pg.Surface
    _asset_negra_turno: pg.Surface
    _asset_blanca_movimiento: pg.Surface
    _asset_negra_movimiento: pg.Surface
    _asset_tapar_texto: pg.Surface
    _asset_celda_oscura : pg.Surface
    _asset_celda_clara : pg.Surface
    _asset_guardar_partida: pg.Surface

    #Botones
    _assetBoton: pg.Surface
    _assetBotonEncima: pg.Surface

    _botonGuardar: pg.Rect

    #Fuentes
    _fuenteTurno: pg.font.Font
    _fuenteMovimientos: pg.font.Font
    _fuenteBotones: pg.font.Font

    #Movimientos
    _inicioTextoMovimientosY: int
    _numeroMovimientos: int
    _segundaColumnaEmpezada: bool
    _terceraColumnaEmpezada: bool

    _fin: bool

    def __init__(self, motor):

        self._motor = motor

        #Iniciar pygame
        pg.init()

        #Configurar ventana de juego
        self._ventana = self.configurarVentana()

        #Cargar assets de la interfaz
        self._asset_fondo, self._asset_tablero, self._asset_blanca_turno, self._asset_negra_turno, self._asset_blanca_movimiento, self._asset_negra_movimiento, self._asset_tapar_texto, self._assetBoton, self._assetBotonEncima, self._asset_celda_oscura, self._asset_celda_clara, self._asset_guardar_partida = self.cargarImagenes()

        #Incializar assets fichas
        Ficha.cargarImagenes()
        FichaSemiTransparente.cargarImagenes()

        #Crear grupo de sprites de las fichas
        self._grupoSpritesFichas = pg.sprite.Group()
        self._nuevaFicha = pg.sprite.Group()

        self._grupoSpritesFichasSemitransparente = pg.sprite.Group()
        self._nuevaFichaSemitransparente = pg.sprite.Group()

        self._angituaFichaSemitransparente = None

        #Cargar fuentes
        self._fuenteTurno = pg.font.Font(c.FUENTE, 30) 
        self._fuenteTurno.set_bold(True)
        self._fuenteMovimientos = pg.font.Font(c.FUENTE, 22) 
        self._fuenteMovimientos.set_bold(True)
        self._fuenteBotones = pg.font.Font(c.FUENTE, 22) 
        self._fuenteBotones.set_bold(True)

        #Movimientos
        self._inicioTextoMovimientosY = c.INICIO_TEXTO_MOVIMIENTOS['y']
        self._numeroMovimientos = 0
        self._segundaColumnaEmpezada = False
        self._terceraColumnaEmpezada = False

        self._fin = False

        self.inicializarInterfaz()

    def configurarVentana(self):
        """Configurar la ventana de la aplicación"""

        ventana = pg.display.set_mode((c.VENTANA_ANCHO, c.VENTANA_LARGO))
        pg.display.set_caption(c.TITULO_INTERFAZ)
        ventana.fill(c.BLANCO_RGB)

        return ventana

    def inicializarInterfaz(self):
        """Inicializar interfaz según las reglas del juego"""

        #Fondo
        self._ventana.blit(self._asset_fondo, (0,0))

        #Tablero
        self._ventana.blit(self._asset_tablero, (0,0))

        #Fichas blancas 
        self.colocarFicha(c.FICHA_BLANCA,3,c.D)
        self.colocarFicha(c.FICHA_BLANCA,4,c.E)

        #Fichas negras
        self.colocarFicha(c.FICHA_NEGRA,4,c.D)
        self.colocarFicha(c.FICHA_NEGRA,3,c.E)

        #Texto turno
        self.dibujarTextoEspaciadoTurno(c.TURNO,c.ESPACIADO_TURNO,c.VERDE_RGB)
        #Empieza el primer jugador
        self.indicarCambioDeTurno(c.P1)

        #Actualizar ventana
        pg.display.update()


    def cargarImagenes(self):
        """Cargar assets"""

        asset_fondo = self.imagen(c.IMG_FONDO_JUEGO,c.VENTANA_ANCHO)
        asset_tablero = self.imagen(c.IMG_TABLERO,700)

        _asset_blanca_turno = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA_TURNO)
        _asset_negra_turno = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA_TURNO)

        _asset_blanca_movimiento = self.imagen(c.IMG_FICHA_BLANCA, c.DIM_FICHA_MOVIMIENTO)
        _asset_negra_movimiento = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA_MOVIMIENTO)

        _asset_tapar_texto = self.imagenDimesiones(c.IMG_TAPA_TEXTO, c.DIM_TAPA_TEXTO['x'], c.DIM_TAPA_TEXTO['y'])

        _asset_boton = self.imagenDimesiones(c.IMG_BOTON,c.ANCHURA_BOTON_GUARDADO,c.ALTURA_BOTON_GUARDADO)
        _asset_boton_encima = self.imagenDimesiones(c.IMG_BOTON_ENCIMA,c.ANCHURA_BOTON_GUARDADO,c.ALTURA_BOTON_GUARDADO)

        _asset_celda_oscura = self.imagen(c.IMG_CELDA_OSCURA,c.DIM_CELDA)
        _asset_celda_clara = self.imagen(c.IMG_CELDA_CLARA,c.DIM_CELDA)

        _asset_guardar_partida = self.imagen(c.IMG_GUARDAR_PARTIDA,c.DIM_BOTON_GUARDADO)

        return asset_fondo, asset_tablero, _asset_blanca_turno, _asset_negra_turno, _asset_blanca_movimiento, _asset_negra_movimiento, _asset_tapar_texto, _asset_boton, _asset_boton_encima, _asset_celda_oscura, _asset_celda_clara, _asset_guardar_partida
    
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
    
    def imagenDimesiones(self,ruta,dimX,dimY):
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
            
    def colocarFicha(self,color:str,fila:int,columna:int):
        """Colocar la ficha en el tablero y actualizar el tablero para que se visualice correctamente"""

        # Convertir fila, columna a coordenadas de píxel
        pixelSupIzq = self.deCeldaAPixel(fila, columna)

        # Crear nueva ficha 
        nueva_ficha = Ficha(color, (fila, columna), pixelSupIzq)

        # Añadir ficha al grupo
        self._grupoSpritesFichas.add(nueva_ficha)
        self._nuevaFicha.add(nueva_ficha)

        #Dibujar ficha
        self._nuevaFicha.draw(self._ventana)
        #Vaciar
        self._nuevaFicha.empty()

        #Actualizar ventana
        pg.display.update()

    def colocarFichaSemitransparente(self,color:str,fila:int,columna:int):
        """Colocar la ficha en el tablero y actualizar el tablero para que se visualice correctamente"""

        # Convertir fila, columna a coordenadas de píxel
        pixelSupIzq = self.deCeldaAPixel(fila, columna)

        # Crear nueva ficha 
        nueva_ficha = FichaSemiTransparente(color, (fila, columna), pixelSupIzq)

        # Añadir ficha al grupo
        self._grupoSpritesFichasSemitransparente.add(nueva_ficha)
        self._nuevaFichaSemitransparente.add(nueva_ficha)

        #Dibujar ficha
        self._nuevaFichaSemitransparente.draw(self._ventana)
        #Vaciar
        self._nuevaFichaSemitransparente.empty()

        #Actualizar ventana
        pg.display.update()

    def eliminarFichaSemitrasparente(self,fila:int,columna:int):
        eliminar = None

        for sprite in self._grupoSpritesFichasSemitransparente:
            if(sprite.pos == (fila,columna)):
                eliminar = sprite
                break
                                
        if (eliminar != None):
                if ((fila,columna) in c.CELDAS_OSCURAS):
                    celda = self._asset_celda_oscura
                else: 
                    celda = self._asset_celda_clara

                self._grupoSpritesFichasSemitransparente.remove(eliminar)

                self._ventana.blit(celda, self.deCeldaAPixel(fila,columna))

                #Actualizar ventana
                pg.display.update()


    def obtenerFichaJugador(self):
        """"Obtener asset de la ficha correspondiente al jugador activo"""

        jugadorActivo = self._motor.getJugadorActivo()

        if (jugadorActivo.getColor() == c.NEGRO):
            colorFicha = c.FICHA_NEGRA
        else:
            colorFicha = c.FICHA_BLANCA
    
        return colorFicha
    
    def cambiarFichasEncerradas(self, celdas):
        """Cambiar sprite de las fichas encerradas por las fichas del jugador actual"""

        colorFicha = self.obtenerFichaJugador()

        for [fila,columna] in celdas:
            self.colocarFicha(colorFicha,fila,columna)

    def dibujarTextoEspaciadoTurno(self,texto,espaciado,color):
        """Dibujar en la interfaz el texto indicador del turno espaciado"""

        dimensionTotal = sum([self._fuenteTurno.size(letra)[0] + espaciado for letra in texto]) - espaciado
        xInicial = c.LOCALIZACION_CENTRO_DERECHA - dimensionTotal
        yInicial = c.ORIGEN_MARGO['y']

        # Renderizar cada letra del texto individualmente con espaciado
        for letra in texto:
            assetLetra = self._fuenteTurno.render(letra, True, color)
            self._ventana.blit(assetLetra, (xInicial, yInicial))
            # Ajustar xInicial para la siguiente letra
            xInicial += assetLetra.get_width() + espaciado

    def dibujarTextoEspaciadoGanador(self,texto,espaciado,color):
        """Dibujar en la interfaz el texto del ganador espaciado"""

        dimensionTotal = sum([self._fuenteTurno.size(letra)[0] + espaciado for letra in texto]) - espaciado
        xInicial = c.LOCALIZACION_CENTRO_DERECHA - dimensionTotal + 120
        yInicial = c.ORIGEN_MARGO['y']

        # Renderizar cada letra del texto individualmente con espaciado
        for letra in texto:
            assetLetra = self._fuenteTurno.render(letra, True, color)
            self._ventana.blit(assetLetra, (xInicial, yInicial))
            # Ajustar xInicial para la siguiente letra
            xInicial += assetLetra.get_width() + espaciado

    def dibujarTextoEspaciadoMovimientos(self,texto,espaciado,color,offset):
        """Dibujar en la interfaz el texto de cada movimiento espaciado"""

        dimensionTotal = sum([self._fuenteMovimientos.size(letra)[0] + espaciado for letra in texto]) - espaciado
        xInicial = c.LOCALIZACION_CENTRO_DERECHA - dimensionTotal + offset
        yInicial = self._inicioTextoMovimientosY

        # Renderizar cada letra del texto individualmente con espaciado
        for letra in texto:
            assetLetra = self._fuenteMovimientos.render(letra, True, color)
            self._ventana.blit(assetLetra, (xInicial, yInicial))
            # Ajustar xInicial para la siguiente letra
            xInicial += assetLetra.get_width() + espaciado

    def dibujarTextoEspaciadoBotones(self,texto,espaciado,color,xBoton, yBoton):
        """Dibujar en la interfaz el texto de un botón espaciado"""

        dimensionTotal = sum([self._fuenteBotones.size(letra)[0] + espaciado for letra in texto]) - espaciado
        alturaTexto = self._fuenteBotones.size(texto)[1]
        xInicial = xBoton + (c.ANCHURA_BOTON_GUARDADO - dimensionTotal) // 2
        yInicial = yBoton + (c.ALTURA_BOTON_GUARDADO //2) - (alturaTexto//1.5)

        # Renderizar cada letra del texto individualmente con espaciado
        for letra in texto:
            assetLetra = self._fuenteBotones.render(letra, True, color)
            self._ventana.blit(assetLetra, (xInicial, yInicial))
            # Ajustar xInicial para la siguiente letra
            xInicial += assetLetra.get_width() + espaciado
    
    def indicarCambioDeTurno(self,jugador:int):
        """Indicar visualmente en la interfaz el turno del jugador activo"""

        if jugador == c.P1:
            assetTurno = self._asset_negra_turno
        else: 
            assetTurno = self._asset_blanca_turno

        #Colocar la ficha 
        self._ventana.blit(assetTurno, (c.LOCALIZACION_CENTRO_DERECHA+20,c.ORIGEN_MARGO['y']))
        #Actualizar ventana
        pg.display.update()

    
    def actualizarInicioTextoMovimientosY(self):
        self._inicioTextoMovimientosY += c.DISTANCIA_TEXTO_MOVIMIENTOS

    def reiniciarInicioTextoMovimientosY(self):
        self._inicioTextoMovimientosY = c.INICIO_TEXTO_MOVIMIENTOS['y']

    def indicarMovimiento(self,jugador:int,fila:int,columna:int):
        """Indicar visualmente el movimiento realizado por el jugador activo"""

        #Comprobar en qué columna escribir el movimiento
        if (self._numeroMovimientos < c.MAXIMO_MOVIMIENTOS_TEXTO):
            offset = c.OFFSET_UNO_MOVIMIENTO
        elif (self._numeroMovimientos < c.MAXIMO_MOVIMIENTOS_TEXTO*2):
            offset = c.OFFSET_DOS_MOVIMIENTO
            if (not self._segundaColumnaEmpezada):
                self.reiniciarInicioTextoMovimientosY()
                self._segundaColumnaEmpezada = True
        else:
            offset = c.OFFSET_DOS_MOVIMIENTO = c.OFFSET_TRES_MOVIMIENTO
            if (not self._terceraColumnaEmpezada):
                self.reiniciarInicioTextoMovimientosY()
                self._terceraColumnaEmpezada = True

        #Mostrar cual es el jugador que ha realizado el movimiento
        if jugador == c.P1:
            assetTurno = self._asset_negra_movimiento
        else: 
            assetTurno = self._asset_blanca_movimiento

        #Colocar la ficha 
        self._ventana.blit(assetTurno, (c.LOCALIZACION_CENTRO_DERECHA-c.SEPARACION_FICHA_TEXTO+offset,self._inicioTextoMovimientosY))
        
        #Mostrar el movimiento realizado
        textoColumna = c.VALOR_COLUMNAS[str(columna)]
        textoFila = c.VALOR_FILAS[str(fila)]
        texto =  str(self._numeroMovimientos + 1) + ". " + textoColumna + textoFila
        self.dibujarTextoEspaciadoMovimientos(texto,c.ESPACIADO_MOVIMIENTOS,c.MARRON_RGB,offset)

        #Incrementar valores necesarios
        self._numeroMovimientos += 1
        self.actualizarInicioTextoMovimientosY()

        #Actualizar ventana
        pg.display.update()

    def dibujaBoton(self,boton: pg.Rect,asset: pg.Surface, texto: str): 
        """Crea el boton en la interfaz"""  

        self._ventana.blit(asset, boton.topleft)
        self.dibujarTextoEspaciadoBotones(texto,c.ESPACIADO_BOTONES,c.MARRON_RGB,boton.x,boton.y)

    def posicionDentroDelTablero(self,pos:tuple[int,int]):

        x = pos[0]
        y = pos[1]

        return (x >= c.ORIGEN_TABLERO['x'] and x <= c.FIN_TABLERO['x']) and (y >= c.ORIGEN_TABLERO['y'] and y <= c.FIN_TABLERO['y'])

    def finPartida(self):

        self._fin = True

        ganador = self._motor.comprobarGanador()
        
        if (ganador == c.EMPATE_ENTRE_JUGADORES):
            #Empate entre jugadores
            nombre = "EMPATE"
            textoGanador = c.EMPATE
            color = c.VERDE_RGB
        elif (ganador == c.JUGADOR1_GANA):
            #Ganan las negras
            nombre = "NEGRAS"
            textoGanador = c.NEGRAS
            color = c.NEGRO_RGB
        else:
            #Ganan las blancas
            nombre = "BLANCAS"
            textoGanador = c.BLANCAS
            color = c.BLANCO_RGB

        #Tapar texto turno
        self._ventana.blit(self._asset_tapar_texto, (c.LOCALIZACION_CENTRO_DERECHA-100,c.ORIGEN_MARGO['y']))

        #Escribir texto del ganador
        self.dibujarTextoEspaciadoGanador(textoGanador,c.ESPACIADO_GANADOR,color)

        self._botonGuardar = pg.Rect(c.LOCALIZACION_CENTRO_DERECHA+120,c.FIN_TABLERO['y']+30, c.DIM_BOTON_GUARDADO, c.DIM_BOTON_GUARDADO)
        self.dibujaBoton(self._botonGuardar,self._asset_guardar_partida, " ")

        #Actualizar ventana
        pg.display.update()  

        rutaProvisional = "../Imagenes/" + nombre + ".png"
        pg.image.save(self._ventana, rutaProvisional)   

        print(textoGanador)

        #Gestionar eventos del botón 
        while (True):
            self.gestionaEventosFinalDePartida(rutaProvisional)

    def gestionaEventosFinalDePartida(self,rutaProvisional:str):

        for event in pg.event.get():
            #Cerrar ventana
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self._botonGuardar.collidepoint(event.pos):
                    #Guardar estado del juego
                    ventanaInvisible = tk.Tk()
                    ventanaInvisible.withdraw()

                    ruta = filedialog.asksaveasfilename(defaultextension=".png",
                        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                        initialdir=os.getcwd(),  # Directorio inicial: directorio de trabajo actual
                        title="Guardar como"
                        )
                    if ruta:
                        # Mueve el archivo de la ubicación temporal a la carpeta seleccionada
                        os.rename(rutaProvisional, ruta)
                        print(f"Captura guardada en: {ruta}")
                    else:
                        print("No se seleccionó ninguna carpeta.") 

    def gestionEventos(self):
        """Gestionar eventos en la interfaz"""
        if (self._fin):
            """Esperar a que el usuario cierre la ventana"""
            for event in pg.event.get():
                #Cerrar ventana
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

        if (not self._fin):
            """El juego sigue en marcha"""
            #Coordenadas del ratón
            pos = pg.mouse.get_pos()

            if(pos != None):

                #Ocultar cursor dentro del tablero
                if (self.posicionDentroDelTablero(pos)):
                    pg.mouse.set_visible(True)
                else: 
                    pg.mouse.set_visible(True)

                fila, columna = self.obtenerCelda(pos)

            if(self._motor.dentroCeldas(fila,columna) and self._motor.obtenerValorCelda(fila,columna) == 0):
                if (self._angituaFichaSemitransparente != (fila,columna)):
                    #Colocar ficha del jugador en la interfaz
                    colorFicha = self.obtenerFichaJugador()
                    self.colocarFichaSemitransparente(colorFicha,fila,columna)

                    #Eliminar antigua ficha semitransparente colocada
                    if (self._angituaFichaSemitransparente != None and self._motor.obtenerValorCelda(self._angituaFichaSemitransparente[0],self._angituaFichaSemitransparente[1]) == 0):
                        self.eliminarFichaSemitrasparente(self._angituaFichaSemitransparente[0], self._angituaFichaSemitransparente[1])

                    self._angituaFichaSemitransparente = (fila,columna)

            if (not self._motor.comprobarPosiblesMovimientos()):
                print("NO PUEDE COLOCAR, CAMBIAR TURNO AL SIGUIENTE")

                #Cambiar el turno al siguiente jugador
                self._motor.cambiarTurno(self._motor.getJugadorActivo())
                self.indicarCambioDeTurno(self._motor.getJugadorActivo().getTurno())

            if (self._motor.comprobarFinJuego()):
                self.finPartida()

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
                        if (self._motor.dentroCeldas(fila,columna) and self._motor.obtenerValorCelda(fila,columna) == 0):
                            
                            #Comprobar si hay fichas que han quedado encerradas
                            celdas = self._motor.fichasContrariasEncerradas(fila,columna)

                            if (len(celdas) > 0):

                                #Indicar que jugador coloca la ficha en el tablero
                                self._motor.modificarValorCelda(fila,columna,self._motor.getJugadorActivo().getTurno())
                                self._motor.aumentaCantidadFichasJugador(self._motor.getJugadorActivo())
                                
                                #Colocar ficha del jugador en la interfaz
                                colorFicha = self.obtenerFichaJugador()
                                self.colocarFicha(colorFicha,fila,columna)  

                                #Indicar movimiento realizado     
                                self.indicarMovimiento(self._motor.getJugadorActivo().getTurno(),fila,columna)

                                #Capturar fichas enemigas
                                self._motor.cambiarValorFichasEncerradas(celdas)
                                self.cambiarFichasEncerradas(celdas)
                                self._motor.modificarCantidadFichasJugador(self._motor.getJugadorActivo(), len(celdas))

                                #Turno del siguiente jugador
                                self._motor.cambiarTurno(self._motor.getJugadorActivo())
                                self.indicarCambioDeTurno(self._motor.getJugadorActivo().getTurno())

                                print(self._motor.getTablero())
                                print(f"Columna: {columna}, fila: {fila}")

    def juega(self):
        """Inicia el juego (incluida la inicialización del tablero)"""

        while(True):
            self.gestionEventos()


                         

