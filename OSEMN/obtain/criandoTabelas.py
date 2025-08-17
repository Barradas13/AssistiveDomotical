from padroes import abcClasses
from observables.observableMediaPipe import ObservableMediaPipe

import time
import pandas as pd
import os

class ColetorDados(abcClasses.Observer):

    dados = []

    def mostrar(self, data):
        print("")
        print("#################")
        print("ear: ", data.ear)
        print("pontos olho:", data.pontos_olho)
        print("tempo: ", data.timestamp)
        print("frame: ", data.frame)
        print("#################")
        print("")

    def update(self, data):

        self.dados.append({
            "frame_idx": data.frame,
            "timestamp": data.timestamp,
            "ear": data.ear,
            "pontos_olho": data.pontos_olho,
            "fps": 1/ (time.time() - data.inicio),
            "tempo_processamento": time.time() - data.inicio,
            "piscando" : data.cor
        })

    def retorna_dados(self):
        return self.dados

#estruturar o projeto com POO e ENG software
if __name__ == "__main__":
    
    for video in os.listdir("AssistiveDomotical\\videos\\"):
        dadosMediaPipe = ColetorDados()
        
        caminho_video = "AssistiveDomotical\\videos\\" + video
        print(f"Processando {caminho_video}")


        print("\nProcesso MediaPipe:")

        olhoMediaPipe = ObservableMediaPipe(caminho_video)
        olhoMediaPipe.attach(dadosMediaPipe)
        olhoMediaPipe.execute()

        print("Processo MediaPipe Concluido!")
        print("Criando Tabela:")

        dfMediaPipe = pd.DataFrame(dadosMediaPipe.retorna_dados())
        dfMediaPipe.to_csv(f"AssistiveDomotical\\OSEMN\\obtain\\tabelasBrutas\\{video}MP.csv", index=False)
