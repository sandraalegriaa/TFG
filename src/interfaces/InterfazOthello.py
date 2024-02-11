from dataclasses import dataclass

import Constantes as c
import pygame as pg
import sys
import math as m

from motores import IMotorDeJuego

@dataclass
class InterfazOthello ():

    #Assets
    _asset_tablero: pg.image
    _asset_blanca: pg.image
    _asset_negra: pg.image
    _asset_blanca_trans: pg.image
    _asset_negra_trans: pg.image
    _asset_fondo: pg.image
    _asset_blanca_turno: pg.image
    _asset_negra_turno: pg.image
    _asset_blanca_movimiento: pg.image
    _asset_negra_movimiento: pg.image

    #Turnos
    _fuenteTurno: pg.font
    _fuenteMovimientos: pg.font

    #Movimientos
    _inicioTextoMovimientosY: int
    _numeroMovimientos: int
    _segundaColumnaEmpezada: bool
    _terceraColumnaEmpezada: bool

    def __init__(self):

        #Iniciar pygame
        pg.init()

        #Configurar ventana de juego
        self._ventana = self.configurarVentana()

        #Cargar assets de la interfaz
        self._asset_fondo, self._asset_tablero, self._asset_blanca, self._asset_negra, self._asset_blanca_trans, self._asset_negra_trans, self._asset_blanca_turno, self._asset_negra_turno, self._asset_blanca_movimiento, self._asset_negra_movimiento = self.cargarImagenes()

        #Cargar fuentes
        self._fuenteTurno = pg.font.Font(c.FUENTE, 30) 
        self._fuenteTurno.set_bold(True)
        self._fuenteMovimientos = pg.font.Font(c.FUENTE, 22) 
        self._fuenteMovimientos.set_bold(True)

        self._inicioTextoMovimientosY = c.INICIO_TEXTO_MOVIMIENTOS['y']
        self._numeroMovimientos = 0
        self._segundaColumnaEmpezada = False
        self._terceraColumnaEmpezada = False

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
        self._ventana.blit(self._asset_blanca, self.deCeldaAPixel(3,c.D))
        self._ventana.blit(self._asset_blanca, self.deCeldaAPixel(4,c.E))

        #Fichas negras
        self._ventana.blit(self._asset_negra, self.deCeldaAPixel(4,c.D))
        self._ventana.blit(self._asset_negra, self.deCeldaAPixel(3,c.E))

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

        asset_blanca = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA)
        asset_negra = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA)

        asset_blanca_trans = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA)
        asset_negra_trans = self.imagen(c.IMG_FICHA_NEGRA,c.DIM_FICHA)

        _asset_blanca_turno = self.imagen(c.IMG_FICHA_BLANCA,c.DIM_FICHA_TURNO)
        _asset_negra_turno = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA_TURNO)

        _asset_blanca_movimiento = self.imagen(c.IMG_FICHA_BLANCA, c.DIM_FICHA_MOVIMIENTO)
        _asset_negra_movimiento = self.imagen(c.IMG_FICHA_NEGRA, c.DIM_FICHA_MOVIMIENTO)

        return asset_fondo, asset_tablero, asset_blanca, asset_negra, asset_blanca_trans, asset_negra_trans, _asset_blanca_turno, _asset_negra_turno, _asset_blanca_movimiento, _asset_negra_movimiento
    
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

    def dibujarTextoEspaciadoTurno(self,texto,espaciado,color):
        """Dibujar en la interfaz el texto del título espaciado"""

        dimensionTotal = sum([self._fuenteTurno.size(letra)[0] + espaciado for letra in texto]) - espaciado
        xInicial = c.LOCALIZACION_CENTRO_DERECHA - dimensionTotal
        yInicial = c.ORIGEN_MARGO['y']

        # Renderizar cada letra del texto individualmente con espaciado
        for letra in texto:
            assetLetra = self._fuenteTurno.render(letra, True, color)
            self._ventana.blit(assetLetra, (xInicial, yInicial))
            # Ajustar xInicial para la siguiente letra
            xInicial += assetLetra.get_width() + espaciado

    def dibujarTextoEspaciadoMovimientos(self,texto,espaciado,color,offset):
        """Dibujar en la interfaz el texto del título espaciado"""

        dimensionTotal = sum([self._fuenteMovimientos.size(letra)[0] + espaciado for letra in texto]) - espaciado
        xInicial = c.LOCALIZACION_CENTRO_DERECHA - dimensionTotal + offset
        yInicial = self._inicioTextoMovimientosY

        # Renderizar cada letra del texto individualmente con espaciado
        for letra in texto:
            assetLetra = self._fuenteMovimientos.render(letra, True, color)
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
        columna = c.VALOR_COLUMNAS[str(columna)]
        fila = c.VALOR_FILAS[str(fila)]
        texto =  str(self._numeroMovimientos + 1) + ". " + columna + fila
        self.dibujarTextoEspaciadoMovimientos(texto,c.ESPACIADO_MOVIMIENTOS,c.MARRON_RGB,offset)

        #Incrementar valores necesarios
        self._numeroMovimientos += 1
        self.actualizarInicioTextoMovimientosY()

        #Actualizar ventana
        pg.display.update()

    def gestionEventos(self, motor: IMotorDeJuego):
        """Gestionar eventos en la interfaz"""
        fin = False

        if (not motor.comprobarPosiblesMovimientos()):
            print("NO PUEDE COLOCAR, CAMBIAR TURNO AL SIGUIENTE")

            #Cambiar el turno al siguiente jugador
            motor.cambiarTurno(motor.getJugadorActivo())
            self.indicarCambioDeTurno(motor.getJugadorActivo().getTurno())

        if (motor.comprobarFinJuego()):
            #TODO: TERMINAR LA PARTIDA CON INTERFAZ PERSONALIZADA
            ganador = motor.comprobarGanador()
            fin = True

            if (ganador == c.EMPATE_ENTRE_JUGADORES):
                #Empate entre jugadores
                pg.image.save(self._ventana, "../Assets/empate.png")
                print("EMPATE")
                pg.quit()
                return fin
            elif (ganador == c.JUGADOR1_GANA):
                #Ganan las negras
                print("GANAN LAS NEGRAS")
                pg.image.save(self._ventana, "../Assets/negras.png")
                pg.quit()
                return fin
            else:
                #Ganan las blancas
                print("GANAN LAS BLANCAS")
                pg.image.save(self._ventana, "../Assets/blancas.png")
                pg.quit()
                return fin

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
                            motor.aumentaCantidadFichasJugador(motor.getJugadorActivo())

                            #Colocar ficha del jugador en la interfaz
                            ficha = self.obtenerFichaJugador(motor)
                            self.colocarFicha(ficha,fila,columna)  

                            #Indicar movimiento realizado     
                            self.indicarMovimiento(motor.getJugadorActivo().getTurno(),fila,columna)

                            #Capturar fichas enemigas
                            motor.cambiarValorFichasEncerradas(celdas)
                            self.cambiarFichasEncerradas(motor, celdas)
                            motor.modificarCantidadFichasJugador(motor.getJugadorActivo(), len(celdas))

                            #Turno del siguiente jugador
                            motor.cambiarTurno(motor.getJugadorActivo())
                            self.indicarCambioDeTurno(motor.getJugadorActivo().getTurno())

                            print(motor.getTablero())
                            print(f"Columna: {columna}, fila: {fila}")

        return fin

                         

