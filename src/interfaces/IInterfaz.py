from dataclasses import dataclass
from typing import Protocol
import Constantes as c
import pygame as pg

@dataclass
class IInterfaz(Protocol):

    _ventana: pg.display


