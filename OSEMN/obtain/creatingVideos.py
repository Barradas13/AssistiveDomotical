import cv2
from pynput import keyboard

# Variável global que marca se 'a' está sendo pressionado
a_pressionado = False

# Função chamada quando uma tecla é pressionada
def ao_pressionar(tecla):
    global a_pressionado
    try:
        if tecla.char == 'a':
            a_pressionado = True
    except AttributeError:
        pass

# Função chamada quando uma tecla é solta
def ao_soltada(tecla):
    global a_pressionado
    try:
        if tecla.char == 'a':
            a_pressionado = False
    except AttributeError:
        pass

# Inicia o listener do teclado
listener = keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltada)
listener.start()

# Captura de vídeo
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = 20
codec = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    r"C:\Users\claudio.barradas\PycharmProjects\Domotic\teste\AssistiveDomotical\videos\felipe.mp4",
    codec, fps, (frame_width, frame_height)
)


print("Gravando... Segure 'a' para ponto verde. Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Desenha o ponto com a cor baseada na variável global
    cor = (0, 255, 0) if a_pressionado else (0, 0, 255)
    cv2.circle(frame, (20, 20), 10, cor, -1)

    cv2.imshow('Webcam', frame)
    out.write(frame)

    # Sai com tecla 'q' detectada pelo OpenCV
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera tudo
cap.release()
out.release()
cv2.destroyAllWindows()
listener.stop()
