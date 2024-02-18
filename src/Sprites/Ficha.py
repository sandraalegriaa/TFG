import pygame as pg

import Constantes as c

class Ficha(pg.sprite.Sprite):
    """Clase para representar una ficha como un sprite."""

    #Assets
    _asset_blanca: pg.image = None
    _asset_negra: pg.image = None

    def __init__(self, color: str, pos: tuple[int], pixelSupIzq: tuple[int]):

        #Incializar el sprite
        super().__init__()

        self._color = color
        self.pos = pos

        if color == 'blanca':
            self.image = self._asset_blanca 
        else:
            self.image = self._asset_negra

        self.rect = self.image.get_rect()
        self.rect.topleft = pixelSupIzq

    @classmethod
    def cargarImagenes(cls):
        """Cargar assets de las fichas para las intancias de la clase Ficha"""

        if not cls._asset_blanca:
            cls._asset_blanca = pg.image.load(c.IMG_FICHA_BLANCA).convert_alpha()
            cls._asset_blanca = pg.transform.scale(cls._asset_blanca, (c.DIM_FICHA, c.DIM_FICHA))
        
        if not cls._asset_negra:
            cls._asset_negra = pg.image.load(c.IMG_FICHA_NEGRA).convert_alpha()
            cls._asset_negra = pg.transform.scale(cls._asset_negra, (c.DIM_FICHA, c.DIM_FICHA))

    