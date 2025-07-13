from padroes.abcClasses import Observer, DataEvent
from observables.observableMediaPipe import ObservableMediaPipe
from observables.observableDlib import ObservablaDlib

import time
import pandas as pd
import keyboard
import threading

class ColetorDados(Observer):

    dados = []

    def __init__(self, biblioteca, metodo):
        self.metodo = metodo
        self.biblioteca = biblioteca

    def mostrar(self, data):
        print("")
        print("#################")
        print("ear: ", data.ear)
        print("tempo: ", data.timestamp)
        print("frame: ", data.frame)
        print("#################")
        print("")

    def update(self, data):

        self.dados.append({
            "frame_idx": data.frame,
            "timestamp": data.timestamp,
            "biblioteca": self.biblioteca,
            "abordagem": self.metodo,
            "ear": data.ear,
            "fps": 1/ (time.time() - data.inicio),
            "tempo_processamento": time.time() - data.inicio,
            "piscando" : keyboard.is_pressed('a')
        })

    def retorna_dados(self):
        return self.dados

#estruturar o projeto com POO e ENG software
if __name__ == "__main__":
    dadosMediaPipe = ColetorDados("mediapipe", "1")
    dadosDlib = ColetorDados("dlib", "2")

    olhoMediaPipe = ObservableMediaPipe(0)
    olhoMediaPipe.attach(dadosMediaPipe)

    olhoDlib = ObservablaDlib(0)
    olhoDlib.attach(dadosDlib)

    #threading.Thread(target=olhoDlib.executar).start()
    olhoMediaPipe.execute()
    #olhoDlib.executar()

    #dfMediaPipe = pd.DataFrame(dadosMediaPipe.retorna_dados())
    #dfMediaPipe.to_csv(r"tabelas\mediaPipe.csv", index=False)

    #dfDlib = pd.DataFrame(dadosDlib.retorna_dados())
    #dfDlib.to_csv(r"tabelas\dlib.csv", index=False)
