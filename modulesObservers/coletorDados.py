from padroes.abcClasses import Observer, DataEvent
from observables.observableMediaPipe import BlinkObserver

import time
import pandas as pd

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
            "tempo_processamento": time.time() - data.inicio
        })

    def retorna_dados(self):
        return self.dados

#estruturar o projeto com POO e ENG software
if __name__ == "__main__":
    teste = ColetorDados("mediapipe", "1")
    video = r'videos\noPattern.mp4'

    olho = BlinkObserver(video)
    olho.attach(teste)


    olho.execute()

    df = pd.DataFrame(teste.retorna_dados())
    df.to_csv(r"tabelas\m1np.csv", index=False)
