from abc import ABC, abstractmethod

class Jugador(ABC):

    def __init__(self, jugador):

        self.jugador = jugador
    
    @abstractmethod
    def decideMovimiento(self):
        pass

        
