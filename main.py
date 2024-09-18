from observadoMainClass import observadorMainClass
from menuMainClass import Menu
import os
import numpy as np

import threading    

if __name__ == "__main__":
    sistema = observadorMainClass(0)
    menu = Menu()
    sistema.attach(menu)
    sistema.calibrar_razao_olhos()
    x = threading.Thread(target=menu.run)  
    x.start()  

    sistema.executar()
