from dataclasses import dataclass
from enum import Enum

class TipoPuntuacion(Enum):
    #Dentro de la ventana alfa-beta (se calcula la puntuación de forma precisa)
    PRECISA = 1
    #Fuera de la ventana por parte de alfa
    FALLO_BAJO = 2
    #Fuera de la ventana por parte de beta
    FALLO_ALTO = 3

@dataclass
class EntradaTabla ():

    #Valor hash para la entrada
    _valorHash: int

    #Tipo de puntuación y puntuacion de la situación en el tablero
    _puntuacion: float
    _tipoPuntuacion: TipoPuntuacion

    #Mejor movimiento a realizar (cálculo previo)
    _mejorMovimiento: tuple[int]

    #Profundidad en la cual fue encontrada la puntuación
    _profundidad: int

    def __init__(self,valorHash,puntuacion,tipoPuntuacion,mejorMovimiento,profundidad):

        self._valorHash = valorHash
        self._puntuacion = puntuacion
        self._tipoPuntuacion = tipoPuntuacion
        self._mejorMovimiento = mejorMovimiento
        self._profundidad = profundidad
    
    def getValorHash(self) -> int:
        return self._valorHash

    def getPuntuacion(self) -> float:
        return self._puntuacion
    
    def getTipoPuntuacion(self) -> TipoPuntuacion:
        return self._tipoPuntuacion
    
    def getMejorMovimiento(self) -> tuple[int]:
        return self._mejorMovimiento
    
    def getProfundidad(self) -> int:
        return self._profundidad
    


