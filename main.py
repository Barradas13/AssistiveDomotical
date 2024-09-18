from observadoMainClass import observadorMainClass
from menuMainClass import Menu
import os
import numpy as np

import threading    

if __name__ == "__main__":
    sistema = observadorMainClass(0)
    sistema.calibrar_razao_olhos()
    menu = Menu()
    sistema.attach(menu)

    x = threading.Thread(target=menu.run)  
    x.start()  

    sistema.executar()
