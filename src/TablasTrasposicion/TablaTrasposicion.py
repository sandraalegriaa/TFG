from dataclasses import dataclass
from EntradaTabla import EntradaTabla
from typing import Optional

@dataclass
class TablaTrasposicion ():

    _tamTabla = 64
    _entradas: list[Optional[EntradaTabla]] = [None] * _tamTabla

    def __init__(self,entradas):
        
        self._entradas = entradas

    def obtenerEntrada(self,valorHash:int) -> Optional[EntradaTabla]:
        """Devuelve una entrada de la tabla"""

        entrada = self._entradas[valorHash % self._tamTabla]
        
        if entrada != None:
            if entrada.getValorHash() == valorHash:
                return entrada
            else: 
                return None
        
    def almacenarEntrada(self,entrada:EntradaTabla):
        """Reemplaza la entrada actual"""
        self._entradas[entrada.getValorHash() % self._tamTabla] = entrada
        
        