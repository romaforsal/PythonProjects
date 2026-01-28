import cv2
import numpy as np


class CameraUtils:
    # Cargamos el clasificador preentrenado de Haar (viene con OpenCV)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    @staticmethod
    def detectar_rostro(frame):
        """Devuelve las coordenadas (x,y,w,h) y la imagen en escala de grises"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = CameraUtils.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces, gray

    @staticmethod
    def imagen_a_bytes(imagen_cv2):
        """Convierte una imagen de OpenCV (numpy array) a bytes para guardar en SQL"""
        # Codificamos la imagen en formato .jpg en memoria
        exito, buffer = cv2.imencode('.jpg', imagen_cv2)
        if exito:
            return buffer.tobytes()  # Esto es lo que va a la BD (BLOB)
        return None

    @staticmethod
    def bytes_a_imagen(blob_bytes):
        """Convierte bytes de la BD de vuelta a una imagen OpenCV"""
        # Convertimos bytes a array de numpy
        nparr = np.frombuffer(blob_bytes, np.uint8)
        # Decodificamos a imagen
        return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)