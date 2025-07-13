from padroes.abcClasses import Observer, DataEvent
from observables.observableMediaPipe import ObservableMediaPipe
from observables.observableDlib import ObservablaDlib

import time
import pandas as pd
import os

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
            "piscando" : data.cor
        })

    def retorna_dados(self):
        return self.dados

#estruturar o projeto com POO e ENG software
if __name__ == "__main__":
    
    for video in os.listdir("videos/"):
        dadosMediaPipe = ColetorDados("mediapipe", "1")
        dadosDlib = ColetorDados("dlib", "2")
        
        caminho_video = "videos/" + video
        print(f"Processando {caminho_video}")


        print("\nProcesso MediaPipe:")

        olhoMediaPipe = ObservableMediaPipe(caminho_video)
        olhoMediaPipe.attach(dadosMediaPipe)
        olhoMediaPipe.execute()

        print("Processo MediaPipe Concluido!")
        print("Criando Tabela:")
        
        dfMediaPipe = pd.DataFrame(dadosMediaPipe.retorna_dados())
        dfMediaPipe.to_csv(f"tabelas/{video}MP.csv", index=False)
        
        print("\nProcesso Dlib:")

        olhoDlib = ObservablaDlib(caminho_video)
        olhoDlib.attach(dadosDlib)
        olhoDlib.executar()

        print("Processo Dlib Concluido!")
        print("Criando Tabela:")
        
        dfDlib = pd.DataFrame(dadosDlib.retorna_dados())
        dfMediaPipe.to_csv(f"tabelas/{video}DLIB.csv", index=False)



