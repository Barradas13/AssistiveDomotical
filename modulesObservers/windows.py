"""for this to work you have to open the OSK of windows go on it´s config and select scan over keys
then you regulate the time and space for scanning"""

import os
from padroes.observerClasses import *
import pyautogui
from observables.observableDlib import observadorMainClass

class Teclado(Observer):
    def __init__(self):
        os.startfile("osk.exe")

    def update(self, subject: Observable, dataEvent:DataEvent) -> None:
        
        if dataEvent.ear < 0.27:
            pyautogui.press("space")
            print("oi")

if __name__ == "__main__":
    sistema = observadorMainClass(1)
    teclado = Teclado()
    sistema.attach(teclado)

    sistema.executar()
