from observables.observableDlib import ObservableDlib
from modulesObservers.menuMainClass import Menu
import os
import numpy as np

import threading    

if __name__ == "__main__":
    sistema = observadorMainClass("video.mp4")
    #sistema.calibrar_razao_olhos()
    #print(sistema.razao_max)
    #print(sistema.limiar)
    #print(sistema.razao_min)

    menu = Menu()
    sistema.attach(menu)

    x = threading.Thread(target=menu.run)
    x.start()

    sistema.executar()