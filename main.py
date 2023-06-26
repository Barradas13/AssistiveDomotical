import cv2
import dlib 
import os
import equacoes
import time
from menu import menu
import observerClasses


#funçao para pegar os frames da webcam, retorna o detector do dlib e o arquivo.dat enviado no parametro
def pegaWebcam(arquivo):
    video_capture = cv2.VideoCapture(0) 

    video_capture.set(int(video_capture.get(5)), 30)

    video_capture.set(int(video_capture.get(3)), 320)
    video_capture.set(int(video_capture.get(3)), 130)
    detector = dlib.get_frontal_face_detector() 
    predictor = dlib.shape_predictor(os.path.join(arquivo)) 

    return video_capture, detector, predictor


#função que reconhece os rostos e verifica o maior destes
def reconhecendoFacesNoFrame(frame):
    frame = cv2.flip(frame,180) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_image = clahe.apply(gray)
    areaMaior = -100
    shapePrincipal = 0

    detections = detector(clahe_image, 1)
    if detections:
        pegarOlhos = True
        #para cada detecção de rostos o algoritimo vai pegar os maiores pontos dos extremos dos x e dos y para assim fazer uma area e verificar qual o maior dos rostos, e apos isso definir um rosto principal
        for k,d in enumerate(detections):
            
            shape = predictor(clahe_image, d)
            for i in range(1,68):  
                #coloca os pontos dos rostos e os numeros dos respectivos              
                cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0,255,0), thickness=-1)
                frame = cv2.putText(frame, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 
                                (0, 0, 255), 1, cv2.LINE_AA, False)
            
            area = (shape.part(15).x - shape.part(1).x) * (shape.part(8).y - shape.part(19).y)

            #verifica a area maior
            if  area > areaMaior:
                areaMaior = area
                shapePrincipal = shape
            else:
                pass
        
        #se o objetivo e pegar os pontos principais dos olhos do rosto principal ele pega e retorna quao fechado ou aberto esta o olho da direira e o olho da esquerda e retorna o frame
        if pegarOlhos:
            EAR_dir, EAR_esq = pegandoPontosDosOlhos(shapePrincipal)
            #frame = frame[shapePrincipal.part(1).x:shapePrincipal.part(15).x, shapePrincipal.part(19).y:shapePrincipal.part(8).y]
            return EAR_dir, EAR_esq, frame
        else:
            return 0,0, frame
    else:
        return 0, 0, frame


#pega os pontos dos olhos do rosto principal e os retorna
def pegandoPontosDosOlhos(shape):
    EAR_esq = equacoes.razaoDistOlhos((shape.part(37).x, shape.part(37).y), 
                                            (shape.part(41).x, shape.part(41).y), 
                                            (shape.part(38).x, shape.part(38).y), 
                                            (shape.part(40).x, shape.part(40).y), 
                                            (shape.part(36).x, shape.part(36).y), 
                                            (shape.part(39).x, shape.part(39).y)) 

    EAR_dir = equacoes.razaoDistOlhos((shape.part(44).x, shape.part(44).y), 
                                            (shape.part(46).x, shape.part(46).y), 
                                            (shape.part(43).x, shape.part(43).y), 
                                            (shape.part(47).x, shape.part(47).y), 
                                            (shape.part(45).x, shape.part(45).y), 
                                            (shape.part(42).x, shape.part(42).y))                                         
    return EAR_dir, EAR_esq



if __name__ == "__main__":
    video_capture, detector, predictor  = pegaWebcam("shape_predictor_68_face_landmarks.dat")
    timeInicial = 0
    olhoFechado = False
    
    subject = observerClasses.ConcreteObservable()

    subject.attach(menu)

    while True:

        ret, frame = video_capture.read()

        EAR_dir, EAR_esq, frame = reconhecendoFacesNoFrame(frame)
        
        #se o olho direito esta fechado vai definir olhoFechado como true, e se esta e a primeira vez do olhoFechado estar fechado vai pegar o tempo inicial

        if EAR_dir < 0.25 and EAR_dir != 0:      
            cv2.circle(frame, (10, 10), 10, (0,255,0), thickness=-1)    
            if not olhoFechado:
                timeInicial = time.time()
            olhoFechado = True
        else:
            cv2.circle(frame, (10, 10), 10, (0,0,255), thickness=-1) 

            #se o olho estivesse fechado mas no momento esta aberto quer dizer que o usuario acabou de abrir o olho, logo se pega o tempo final e faz o calculo do tempo que o olho ficou fechado

            if olhoFechado:
                timeFinal = time.time()
                tempo = timeFinal - timeInicial
                olhoFechado = False

                if tempo > 0.2:
                    subject.some_business_logic(True, tempo)
                
            piscou, tempo = False, 0

        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
       
        
    video_capture.release()
    cv2.destroyAllWindows()
