import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_con=0.7, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        # Inicialización de MediaPipe Solutions
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )

    def find_hands(self, img, draw=True):
        """Detecta las manos y dibuja las conexiones (21 puntos)"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    # Dibujamos los 21 puntos y sus conexiones
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img):
        """Extrae la lista de coordenadas de los 21 puntos"""
        self.lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            # Procesamos solo la primera mano detectada
            my_hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                # Convertimos las coordenadas normalizadas (0.0 a 1.0) a píxeles
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
        return self.lm_list