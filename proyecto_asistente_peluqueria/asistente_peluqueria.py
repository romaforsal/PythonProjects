import os
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Cargar la API Key desde el archivo .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    messagebox.showerror("Error", "No se encontró la API Key. Revisa tu archivo .env")
    exit()

# 2. Configurar la API de Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")  # Puedes cambiarlo por otro modelo si lo deseas

# 3. Cargar el contexto (servicios de la peluquería)
with open("servicios.txt", "r", encoding="utf-8") as f:
    contexto_peluqueria = f.read()

# 4. Función para enviar la consulta a Gemini
def obtener_respuesta():
    pregunta = entrada_usuario.get()

    if not pregunta.strip():
        messagebox.showwarning("Atención", "Por favor, escribe una pregunta.")
        return

    try:
        # Enviamos el contexto y la pregunta
        prompt = f"Eres un asistente de peluquería. Usa esta información para responder:\n{contexto_peluqueria}\n\nPregunta: {pregunta}"

        respuesta = model.generate_content(prompt)

        # Manejar formato JSON si la respuesta viene en ese formato
        try:
            data = json.loads(respuesta.text)
            texto_respuesta = data.get("respuesta", "No se encontró información en el JSON.")
        except json.JSONDecodeError:
            texto_respuesta = respuesta.text  # Si no es JSON, mostramos el texto directamente

        salida_texto.config(state="normal")
        salida_texto.insert(tk.END, f"Tú: {pregunta}\n")
        salida_texto.insert(tk.END, f"Asistente: {texto_respuesta}\n\n")
        salida_texto.config(state="disabled")

        entrada_usuario.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# 5. Interfaz gráfica (Tkinter)
ventana = tk.Tk()
ventana.title("Asistente Virtual de Peluquería 💇‍♀️")
ventana.geometry("600x400")
ventana.config(bg="#f2f2f2")

# Cuadro de salida
salida_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=70, height=15, state="disabled", bg="#ffffff")
salida_texto.pack(padx=10, pady=10)

# Entrada del usuario
entrada_usuario = tk.Entry(ventana, width=70)
entrada_usuario.pack(padx=10, pady=5)

# Botón de enviar
boton_enviar = tk.Button(ventana, text="Enviar", bg="#4CAF50", fg="white", command=obtener_respuesta)
boton_enviar.pack(pady=10)

# 🔹 NUEVO: permitir enviar con la tecla Enter
def enviar_con_enter(event):
    obtener_respuesta()

entrada_usuario.bind("<Return>", enviar_con_enter)

ventana.mainloop()
