#https://refactoring.guru/design-patterns/observer/python/example

from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


#vai ser os dados que os observadores vão receber
class DataEvent():
    piscou = False
    tempo = 0
###############################################


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

###############################################

"""
    isso vai ser a piscada, quando piscar vai notificar os observadores (menu)
"""
class ConcreteObservable(Observable):
    
    _observers: List[Observer] = []


    #coloca novos observadores
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)


    #remove os observadores
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    #atualiza os observadores com os dados restornados, piscou e tempo
    def notify(self, dataEvent:DataEvent) -> None:
        
        print("Observable: Notifying observers...")
        for observer in self._observers:
            observer.update(self, dataEvent)

    #loop para verificar a piscada, quando piscar vai notificar os observadores
    def some_business_logic(self, piscou, tempo) -> None:
      
        print("\nSubject: I'm doing something important.")      
        dataEvent = DataEvent()
        dataEvent.piscou = piscou
        dataEvent.tempo = tempo

        self.notify(dataEvent)


"""
    Isso vai ser o menu
"""

class ConcreteObserverA(Observer):
    selection = 1

    #executa a ação quando é notificado
    def update(self, subject: Observable,  dataEvent:DataEvent) -> None:
        pass


if __name__ == "__main__":

    subject = ConcreteObservable()
    menu = ConcreteObserverA()

    subject.attach(menu)

    subject.some_business_logic(False, 0.12)