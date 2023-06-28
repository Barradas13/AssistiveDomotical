from observadorMainClass import observadorMainClass
from menuMainClass import Menu


import threading    

if __name__ == "__main__":
    sistema = observadorMainClass(0)
    menu = Menu()
    sistema.attach(menu)
  
    x = threading.Thread(target=menu.run)  
    x.start()  
    
    sistema.executar()