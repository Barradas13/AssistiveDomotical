import threading
import wx
from observables import observableDlib
from modulesObservers.menuMainClass import Menu

if __name__ == "__main__":
    app = wx.App(False)

    menu = Menu()

    sistema = observableDlib.ObservableDlib(0)
    sistema.attach(menu)

    thread_sistema = threading.Thread(target=sistema.executar, daemon=True)
    thread_sistema.start()

    app.MainLoop()
