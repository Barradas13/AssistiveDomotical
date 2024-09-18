import numpy as np

import observerClasses
import cv2
import dlib
import os
import equacoes
from observerClasses import Observable, Observer, DataEvent
import time


def pegaWebcam(arquivo, video):
    video_capture = video

    video_capture.set(int(video_capture.get(5)), 30)

    video_capture.set(int(video_capture.get(3)), 1080)
    video_capture.set(int(video_capture.get(3)), 640)
    detector = dlib.get_frontal_face_detector() 
    predictor = dlib.shape_predictor(os.path.join(arquivo)) 
    
    return video_capture, detector, predictor

class observadorMainClass(Observable):

    def __init__(self, modoCapture) -> None:
        video = cv2.VideoCapture(modoCapture)
        self._observers = []
        self.video_capture, self.detector, self.preditor = pegaWebcam("shape_predictor_68_face_landmarks.dat", video)
        self.olhoFechado = False
        self.tPiscou = 0
        self.pre_timeFrame = 0
        self.new_timeFrame = 0
        self.resized_image = 0
        self.EAR_dir = 0
        self.EAR_esq = 0
        self.contador = 0

    #coloca novos observadores
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    #remove os observadores
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    #atualiza os observadores com os dados restornados, piscou e tempo
    def notify(self, dataEvent:DataEvent) -> None:
        
        print("Observable: Notifying observers...")
        for observer in self._observers:
            observer.update(self, dataEvent)

    def reconhecendoFacesNoFrame(self):

        if self.detections:
            self.verificandoMaiorFace()
            self.pegandoPontosDosOlhos()

    def verificandoMaiorFace(self):
        areaMaior = 0
        
        for k,d in enumerate(self.detections):
            shape = self.preditor(self.clahe_image, d)
            
            
            area = (shape.part(15).x - shape.part(1).x) * (shape.part(8).y - shape.part(19).y)

            #verifica a area maior
            if  area > areaMaior:
                areaMaior = area
                self.shapePrincipal = shape
            else:
                pass

        for i in range(1,68):  
                #coloca os pontos dos rostos e os numeros dos respectivos              
            cv2.circle(self.frame, (self.shapePrincipal.part(i).x, self.shapePrincipal.part(i).y), 1, (0,255,0), thickness=-1)
            self.frame = cv2.putText(self.frame, str(i), (self.shapePrincipal.part(i).x, self.shapePrincipal.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                (0, 0, 255), 1, cv2.LINE_AA, False)
    

    def pegandoPontosDosOlhos(self):
        self.EAR_dir = equacoes.razaoDistOlhos((self.shapePrincipal.part(37).x, self.shapePrincipal.part(37).y), 
                                                (self.shapePrincipal.part(41).x, self.shapePrincipal.part(41).y), 
                                                (self.shapePrincipal.part(38).x, self.shapePrincipal.part(38).y), 
                                                (self.shapePrincipal.part(40).x, self.shapePrincipal.part(40).y), 
                                                (self.shapePrincipal.part(36).x, self.shapePrincipal.part(36).y), 
                                                (self.shapePrincipal.part(39).x, self.shapePrincipal.part(39).y)) 

        self.EAR_esq = equacoes.razaoDistOlhos((self.shapePrincipal.part(44).x, self.shapePrincipal.part(44).y), 
                                                (self.shapePrincipal.part(46).x, self.shapePrincipal.part(46).y), 
                                                (self.shapePrincipal.part(43).x, self.shapePrincipal.part(43).y), 
                                                (self.shapePrincipal.part(47).x, self.shapePrincipal.part(47).y), 
                                                (self.shapePrincipal.part(45).x, self.shapePrincipal.part(45).y), 
                                                (self.shapePrincipal.part(42).x, self.shapePrincipal.part(42).y))                                         

    def verificacaoEnvioParaObserver(self):
        if self.detections:

            if self.detectar_piscada():
                if not self.olhoFechado:
                    self.tPiscou = time.time()
                    self.olhoFechado = True

                cv2.circle(self.frame, (10, 10), 10, (0,255,0), thickness=-1)
            else:
                cv2.circle(self.frame, (10, 10), 10, (0,0,255), thickness=-1) 

                if self.olhoFechado:
                    self.olhoFechado = False

                    if ( time.time() - self.tPiscou) > 0.5:
                        print("Piscou")
                        dados = DataEvent()
                        dados.tempo = time.time() - self.tPiscou
                        print("tempo evento:", time.time() - self.tPiscou)

                        self.notify(dados)

                    self.tPiscou = 0
    
    def setandoFrame(self):
        self.frame = cv2.flip(self.frame, 180)
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.clahe_image = self.clahe.apply(self.gray)

    def pegandoFrame(self):
        self.ret, self.frame = self.video_capture.read()

    def configurandoDetector(self):
        self.detections = self.detector(self.clahe_image, 0)

    def configurandoFrameMostrar(self):
        self.new_timeFrame = time.time()
        self.fps = 1 / (self.new_timeFrame - self.pre_timeFrame)
        self.pre_timeFrame = self.new_timeFrame
        self.fps = int(self.fps)
        cv2.putText(self.frame, str(self.fps), (8, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 4)

    def mostraFrame(self):
        cv2.imshow('img', self.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            dados = DataEvent()
            dados.tempo = False
            dados.piscou = False
            self.notify(dados)
            return 1

    def calibrar_razao_olhos(self, amostras=100):

        self.razoes_olhos = []
        print("Calibração: Por favor, pisque várias vezes...")

        self.razao_olhos = self.EAR_dir()
        self.razoes_olhos.append(self;razao_olhos)

        self.razao_min = np.min(razoes_olhos)
        self;razao_max = np.max(razoes_olhos)

        # Definir limiar para olhos abertos/fechados baseado no ciclo de piscadas do usuário
        self.limiar = (razao_min + razao_max) / 2

    def detectar_piscada(self):

        # Verifica se a razão dos olhos atual indica olhos fechados
        if self.EAR_dir <= self.limiar:
            return False  # Olhos fechados
        return True  # Olhos abertos

    def executar(self):
        while True:

            self.pegandoFrame()
            self.setandoFrame()

            self.configurandoDetector()
            self.reconhecendoFacesNoFrame()
            self.configurandoFrameMostrar()
            self.verificacaoEnvioParaObserver()

            if self.mostraFrame():
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    sistema = observadorMainClass("video.mp4")
    sistema.executar()
