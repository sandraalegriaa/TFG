from dataclasses import dataclass, field
from .EntradaTabla import EntradaTabla
from typing import Optional
import numpy as np
@dataclass
class TablaTrasposicion ():

    _tamTabla = 16000000
    _entradas: list[Optional[EntradaTabla]] = field(default_factory=lambda: [None] * 16000000)

    def obtenerEntrada(self,valorHash) -> Optional[EntradaTabla]:
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
        
        