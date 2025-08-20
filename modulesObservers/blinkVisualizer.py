import cv2
import numpy as np
from padroes.abcClasses import Observer
from observables.observableMediaPipe import ObservableMediaPipe
import pandas as pd
from joblib import load
import  time


class BlinkVisualizer(Observer):
    def __init__(self, model, output_path="saida.mp4", fps=25):
        self.model = model
        self.ears_anteriores = []
        self.writer = None
        self.output_path = output_path
        self.fps = fps
        self.tempos = []

    def update(self, dataEvent):
        start_time = time.perf_counter()

        if self.writer is None:
            height, width, _ = dataEvent.image.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(self.output_path, fourcc, 15, (width, height))  # força 15fps no vídeo

        # Adiciona o EAR atual ao histórico
        self.ears_anteriores.append(dataEvent.ear)
        if len(self.ears_anteriores) > 5:
            self.ears_anteriores.pop(0)

        # Só prediz quando temos 5 valores
        if len(self.ears_anteriores) == 5:
            features = pd.DataFrame([self.ears_anteriores],
                                    columns=["ear1", "ear2", "ear3", "ear4", "ear5"])

            inicio = time.perf_counter()
            piscando = self.model.predict(features)[0]
            fim = time.perf_counter()

            print(f"Tempo de predição: {(fim - inicio) * 1000:.2f} ms")
            self.tempos.append(fim - inicio)

            # Desenha bolinha no canto superior esquerdo do frame
            color = (0,255,0) if piscando == 1 else (0,0,255)
            cv2.circle(dataEvent.image, (50,50), 20, color, -1)

        # Salva o frame no vídeo
        self.writer.write(dataEvent.image)

        elapsed = time.perf_counter() - start_time
        delay = max(0, (1 / 15) - elapsed)  # tempo que falta até completar 1/15s
        time.sleep(delay)

        # Mostra o frame atualizado
        cv2.imshow("Video Piscando", dataEvent.image)
        cv2.waitKey(1)

    # Para liberar o vídeo quando terminar
    def release(self):
        if self.writer is not None:
            self.writer.release()
            print(f"Vídeo salvo em: {self.output_path}")
            print(np.mean(self.tempos))

# Carrega modelo
model = load("final_model.joblib")

# Cria visualizador e ObservableMediaPipe
visualizer = BlinkVisualizer(model)
obs_mp = ObservableMediaPipe(0)
obs_mp.attach(visualizer)

# Executa captura
try:
    obs_mp.execute()
finally:
    visualizer.release()
    cv2.destroyAllWindows()
