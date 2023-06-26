from observadorMainClass import observadorMainClass
from menuMainClass import Menu

if __name__ == "__main__":
    sistema = observadorMainClass(0)
    menu = Menu()

    sistema.attach(menu)
    menu.run()
    sistema.executar()