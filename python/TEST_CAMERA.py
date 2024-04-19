#TEST_CAMERA.py

import cv2
import time
import os

# Crea un objeto VideoCapture para capturar frames de la cámara
cap = cv2.VideoCapture(0)

# Crea una carpeta para guardar los frames capturados
folder_name = 'captured_frames'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Inicializa el contador de frames y el tiempo de espera
frame_count = 0
wait_time = 1  # en segundos

# Captura frames de la cámara hasta que el usuario presione la tecla 'q'
while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()

    # Comprueba si el frame fue capturado correctamente
    if not ret:
        print('Error: no se pudo capturar el frame')
        break

    # Incrementa el contador de frames
    frame_count += 1

    # Guarda el frame en la carpeta especificada
    filename = os.path.join(folder_name, f'frame_{frame_count}.jpg')
    cv2.imwrite(filename, frame)

    # Muestra el frame capturado en una ventana
    cv2.imshow('Frame', frame)

    # Espera un segundo antes de capturar el siguiente frame
    time.sleep(wait_time)

    # Comprueba si el usuario ha presionado la tecla 'q' para salir del ciclo while
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()
