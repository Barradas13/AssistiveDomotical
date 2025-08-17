import threading
from observables import observableMediaPipe

if __name__ == "__main__":
    sistema = observableMediaPipe.ObservableMediaPipe(0)
    sistema.execute()
