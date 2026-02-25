import speech_recognition as sr
import time


class VoiceService:
    """
    Patrón Facade: Interfaz simplificada para el reconocimiento de voz.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def capturar_y_reconocer(self):
        """Captura audio del micrófono y devuelve el texto y métricas simuladas."""
        with sr.Microphone() as source:
            print("Ajustando ruido de fondo... Habla ahora.")
            self.recognizer.adjust_for_ambient_noise(source)  # Gestiona ruido de fondo [cite: 56]

            inicio = time.time()
            try:
                audio = self.recognizer.listen(source, timeout=5)
                # Envía los datos a un motor (Google) para traducción [cite: 58]
                texto = self.recognizer.recognize_google(audio, language="es-ES")
                latencia = round(time.time() - inicio, 2)

                # Simulamos un grado de confianza (Google Web Speech API básica no lo da por defecto en Python)
                confianza = 0.95

                return {"status": "OK", "texto": texto.lower(), "confianza": confianza, "latencia": f"{latencia}s"}

            except sr.UnknownValueError:
                return {"status": "ERROR", "motivo": "No se entendió el audio"}
            except sr.RequestError:
                return {"status": "ERROR", "motivo": "Error de conexión con el servicio"}
            except Exception as e:
                return {"status": "ERROR", "motivo": str(e)}