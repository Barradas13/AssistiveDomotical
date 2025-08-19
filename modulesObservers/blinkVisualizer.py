import cv2
import numpy as np
from padroes.abcClasses import Observer

class BlinkVisualizer(Observer):
    def __init__(self, model):
        self.model = model
        self.ears_anteriores = []

    def update(self, dataEvent):
        # Adiciona o EAR atual ao histórico
        self.ears_anteriores.append(dataEvent.ear)
        
        # Mantém somente os últimos 5 EARs
        if len(self.ears_anteriores) > 5:
            self.ears_anteriores.pop(0)

        # Só prediz quando temos 5 valores
        if len(self.ears_anteriores) == 5:
            features = np.array(self.ears_anteriores).reshape(1, -1)  # 1 amostra, 5 features
            piscando = self.model.predict(features)[0]

            # Desenha bolinha no canto superior esquerdo do frame
            color = (0,255,0) if piscando == 1 else (0,0,255)  # verde = piscando, vermelho = não piscando
            cv2.circle(dataEvent.image, (50,50), 20, color, -1)  # -1 preenche o círculo

        # Mostra o frame atualizado
        cv2.imshow("Video Piscando", dataEvent.image)
        cv2.waitKey(1)

from joblib import load

model = load("modelo_piscando.joblib")

visualizer = BlinkVisualizer(model)

obs_mp = ObservableMediaPipe(0)

# Anexa o visualizer como observador
obs_mp.attach(visualizer)

# Executa captura e notificação
obs_mp.execute()
