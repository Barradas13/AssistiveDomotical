
from padroes.abcClasses import *

import cv2
import mediapipe as mp
import math
import numpy as np
import  time

#x and y are between 0 and 1 (like a percentage of width and height) so we need to normalize it
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

class ObservableMediaPipe(Observable):
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        print("Subject: Detached an observer.")
        self._observers.remove(observer)

    def notify(self,dataEvent:DataEvent) -> None:
        for observer in self._observers:
            observer.update(dataEvent)

    def __init__(self, modoCaptura):
        self._observers = []

        self.cap = cv2.VideoCapture(modoCaptura)

        # just 25 fps
        self.cap.set(cv2.CAP_PROP_FPS, 25.0)

        # adjusting to camera's height and width
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.mp_face_mesh = mp.solutions.face_mesh
        self.blinkAtributes()

        self.comeco = time.time()
        self.inicioFrame = 0

    def blinkAtributes(self):
        self.ratios = []

        self.frameCount = 1

    def confFaceDetection(self):

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True, #this is not necessary (test without it)
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def gettingResults(self):
        # need to fist interpret it in RGB because of mediapipe
        self.image.flags.writeable = False
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # Run face detection and get 468 face landmarks
        results = self.face_mesh.process(self.image)

        # returns to BGR to openCV
        self.image.flags.writeable = True
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

        return results

    def getSpecificPoint(self, point):
        return _normalized_to_pixel_coordinates(self.face_landmarks[point].x, self.face_landmarks[point].y, self.width, self.height)

    def gettingEyesPoints(self):
        self.supEyeCoord = self.getSpecificPoint(159)
        self.infEyeCoord = self.getSpecificPoint(145)
        self.latEyeCoord = self.getSpecificPoint(33)
        self.latEye2Coord = self.getSpecificPoint(133)

    def gettingDists(self):
        self.distSupInf = math.sqrt((self.supEyeCoord[0] - self.infEyeCoord[0]) ** 2 + (self.supEyeCoord[1] - self.infEyeCoord[1]) ** 2)
        self.distLats = math.sqrt((self.latEye2Coord[0] - self.latEyeCoord[0]) ** 2 + (self.latEye2Coord[1] - self.latEyeCoord[1]) ** 2)

        return self.distLats/ (self.distSupInf + 0.001)

    def gettingRatio(self):
        self.gettingEyesPoints()
        self.ratio = self.gettingDists()

        if self.ratio <= 0:
            self.ratio = self.ratios[0]

        self.ratios.append(self.ratio)

        if (len(self.ratios) == 5):
            self.ratios.pop(0)

        self.mediaRatio = np.mean(self.ratios)
        self.ratioMapped = self.mediaRatio * -1

    def arrumaDadosNotify(self):

        dados = DataEvent()
        dados.ear = self.ratioMapped
        dados.timestamp = time.time() - self.comeco
        dados.frame = self.frameCount
        dados.inicio = self.inicioFrame

        b, g, r = self.image[20, 20]

        if r > g and r > b:
            dados.cor = "vermelho"
        elif g > r and g > b:
            dados.cor = "verde"
        else:
            dados.cor = "indefinido"
            
        self.notify(dados)

    def execute(self):
        font = cv2.FONT_HERSHEY_SIMPLEX

        try:
            self.confFaceDetection()
        except TypeError as e:
            cv2.putText(self.image, str("nenhum rosto encontrado"), (50, 100), font, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

        while self.cap.isOpened():
            success, self.image = self.cap.read()
            self.inicioFrame = time.time()
            if not success:
                print("Ignoring empty camera frame.")
                break

            results = self.gettingResults()

            if (results.multi_face_landmarks):
                self.face_landmarks = results.multi_face_landmarks[0].landmark
            else:
                self.face_landmarks = None

            try:
                self.gettingRatio()

                self.arrumaDadosNotify()

                cv2.line(self.image, self.supEyeCoord, self.infEyeCoord, (255, 0, 0), 4)
                cv2.line(self.image, self.latEyeCoord, self.latEye2Coord, (0, 0, 255), 4)


                cv2.putText(self.image, str(self.ratioMapped), (50, 100), font, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)


            except TypeError as e:
                cv2.putText(self.image, str("nenhum rosto encontrado"), (50, 100), font, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)

            cv2.imshow('MediaPipe Face Mesh', self.image)
            self.frameCount += 1

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
