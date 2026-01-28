import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from src.utils.camera_utils import CameraUtils
from src.usuario_dao import UsuarioDAO
import numpy as np


class BioPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioPass DAO - Sistema de Acceso")
        self.root.geometry("800x600")

        # Variables
        self.cap = cv2.VideoCapture(0)
        self.rostro_detectado = None  # Aquí guardaremos temporalmente la cara recortada

        # UI Layout
        self.panel_video = tk.Label(root)
        self.panel_video.pack(pady=10)

        self.entry_nombre = tk.Entry(root, font=("Arial", 14))
        self.entry_nombre.pack(pady=5)
        self.entry_nombre.insert(0, "Introduce tu nombre")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Registrar Usuario", command=self.registrar, bg="#4CAF50", fg="white").pack(
            side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Login (Entrenar & Reconocer)", command=self.login, bg="#2196F3", fg="white").pack(
            side=tk.LEFT, padx=10)

        # Iniciar loop de video
        self.mostrar_video()

    def mostrar_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Detección de rostros en tiempo real
            rostros, gray = CameraUtils.detectar_rostro(frame)

            for (x, y, w, h) in rostros:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Guardamos la región de interés (ROI) por si el usuario pulsa registrar
                self.rostro_detectado = frame[y:y + h, x:x + w]

            # Convertir para Tkinter
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            self.panel_video.imgtk = img_tk
            self.panel_video.configure(image=img_tk)

        self.root.after(10, self.mostrar_video)

    def registrar(self):
        nombre = self.entry_nombre.get()
        if not nombre or self.rostro_detectado is None:
            messagebox.showwarning("Error", "Debes escribir un nombre y debe haber una cara visible.")
            return

        # 1. Convertir imagen actual a bytes
        foto_bytes = CameraUtils.imagen_a_bytes(self.rostro_detectado)

        # 2. Llamar al DAO (El traductor)
        if UsuarioDAO.registrar_usuario(nombre, foto_bytes):
            messagebox.showinfo("Éxito", f"Usuario {nombre} guardado en BD.")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la BD.")

    def login(self):
        # 1. Obtener datos crudos del DAO
        usuarios = UsuarioDAO.obtener_todos()
        if not usuarios:
            messagebox.showinfo("Info", "No hay usuarios registrados.")
            return

        print(f"Entrenando con {len(usuarios)} usuarios...")

        # 2. Preparar datos para el reconocedor LBPH
        rostros_entrenamiento = []
        ids = []
        mapa_nombres = {}  # Para traducir ID -> Nombre

        for usuario in usuarios:
            user_id, nombre, blob = usuario
            # Convertir BLOB a Imagen para entrenar
            imagen = CameraUtils.bytes_a_imagen(blob)

            if imagen is not None:
                rostros_entrenamiento.append(imagen)
                ids.append(user_id)
                mapa_nombres[user_id] = nombre

        # 3. Entrenar el reconocedor (En memoria)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(rostros_entrenamiento, np.array(ids))

        # 4. Predecir (Usamos el rostro actual de la cámara)
        if self.rostro_detectado is not None:
            gray_actual = cv2.cvtColor(self.rostro_detectado, cv2.COLOR_BGR2GRAY)
            id_predicho, confianza = recognizer.predict(gray_actual)

            # Confianza: en LBPH, menor número = mayor coincidencia (distancia)
            if confianza < 70:
                nombre_detectado = mapa_nombres.get(id_predicho, "Desconocido")
                messagebox.showinfo("Acceso Concedido", f"Bienvenido, {nombre_detectado}!")
            else:
                messagebox.showerror("Acceso Denegado", "No te reconozco.")
        else:
            messagebox.showwarning("Cuidado", "Ponte frente a la cámara.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()