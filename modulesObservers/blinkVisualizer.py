import cv2
import numpy as np
from padroes.abcClasses import Observer
from observables.observableMediaPipe import ObservableMediaPipe
import pandas as pd
from joblib import load

class BlinkVisualizer(Observer):
    def __init__(self, model, output_path="saida.mp4", fps=25):
        self.model = model
        self.ears_anteriores = []
        self.writer = None
        self.output_path = output_path
        self.fps = fps

    def update(self, dataEvent):
        # Inicializa o VideoWriter na primeira chamada
        if self.writer is None:
            height, width, _ = dataEvent.image.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # codec mp4
            self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))

        # Adiciona o EAR atual ao histórico
        self.ears_anteriores.append(dataEvent.ear)
        if len(self.ears_anteriores) > 5:
            self.ears_anteriores.pop(0)

        # Só prediz quando temos 5 valores
        if len(self.ears_anteriores) == 5:
            features = pd.DataFrame([self.ears_anteriores],
                                    columns=["ear1", "ear2", "ear3", "ear4", "ear5"])
            piscando = self.model.predict(features)[0]

            # Desenha bolinha no canto superior esquerdo do frame
            color = (0,255,0) if piscando == 1 else (0,0,255)
            cv2.circle(dataEvent.image, (50,50), 20, color, -1)

        # Salva o frame no vídeo
        self.writer.write(dataEvent.image)

        # Mostra o frame atualizado
        cv2.imshow("Video Piscando", dataEvent.image)
        cv2.waitKey(1)

    # Para liberar o vídeo quando terminar
    def release(self):
        if self.writer is not None:
            self.writer.release()
            print(f"Vídeo salvo em: {self.output_path}")

# Carrega modelo
model = load("modelo_piscando.joblib")

# Cria visualizador e ObservableMediaPipe
visualizer = BlinkVisualizer(model)
obs_mp = ObservableMediaPipe("bruno.mp4")
obs_mp.attach(visualizer)

# Executa captura
try:
    obs_mp.execute()
finally:
    visualizer.release()
    cv2.destroyAllWindows()
