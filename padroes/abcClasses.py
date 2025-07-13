#https://refactoring.guru/design-patterns/observer/python/example

from __future__ import annotations
from abc import ABC, abstractmethod
import cv2

#vai ser os dados que os observadores vão receber
class DataEvent():
    ear = 0
    frame = 0
    timestamp = 0
    inicio = 0

#cria o observavel que tem funções para colocar tirar e notificar
class Observable(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self,dataEvent:DataEvent) -> None:
       pass

class Observer(ABC):   

    @abstractmethod
    def update(self, subject: Observable, dataEvent:DataEvent) -> None:
         pass
