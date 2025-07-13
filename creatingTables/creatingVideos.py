import cv2
import keyboard

# Abre a webcam
cap = cv2.VideoCapture(0)

# Verifica se abriu corretamente
if not cap.isOpened():
    print("Erro ao acessar a webcam.")
    exit()

# Parâmetros do vídeo
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = 20
codec = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('saida.avi', codec, fps, (frame_width, frame_height))

# Estado da cor do ponto
ponto_verde = False

print("Gravando... Pressione 'q' para sair. Pressione 'a' para mudar a cor do ponto.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Define a cor do ponto
    cor_ponto = (0, 255, 0) if keyboard.is_pressed("a") else (0, 0, 255)  # Verde se True, senão Vermelho

    # Desenha o ponto no canto superior esquerdo
    cv2.circle(frame, center=(20, 20), radius=10, color=cor_ponto, thickness=-1)

    # Mostra o frame
    cv2.imshow('Webcam', frame)

    # Grava o frame no vídeo
    out.write(frame)

    # Captura a tecla pressionada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
# Libera os recursos
cap.release()
out.release()
cv2.destroyAllWindows()
