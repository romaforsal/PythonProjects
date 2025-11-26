import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv

# --- 1. Cargar la Clave API y Configurar el Modelo ---

# Cargar variables de entorno (buscará el archivo .env)
load_dotenv()

API_KEY = os.getenv('API_KEY')

# Verificar si la API Key existe
if not API_KEY:
    # Mostrar un error en una ventana emergente si Tkinter ya está inicializado
    # o imprimir en la consola antes de que inicie.
    print("Error: No se encontró la variable de entorno API_KEY.")
    print("Asegúrate de crear un archivo .env y añadir 'API_KEY=tu_clave_api_aqui'.")
    # Es útil mostrar este error en una ventana emergente si es posible
    # Para este script, saldremos antes de iniciar la GUI.
    messagebox.showerror("Error de Configuración",
                         "No se encontró la API_KEY.\n"
                         "Asegúrate de crear un archivo .env con tu clave.")
    sys.exit("Script detenido por falta de API_KEY.")

try:
    # Configurar la API de Google
    genai.configure(api_key=API_KEY)

    # Configuración del modelo
    # Usamos 'gemini-1.5-flash' por ser rápido y eficiente para chat y Q&A
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    # Inicializar el modelo
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config)

except Exception as e:
    messagebox.showerror("Error de API",
                         f"No se pudo configurar la API de Gemini.\n"
                         f"Verifica tu API Key y la conexión a internet.\n\nError: {e}")
    sys.exit("Error al inicializar Gemini.")


# --- 2. Contexto de la Peluquería (In-Context Learning) ---

# Esta es la información clave que "entrena" al modelo en tiempo real.
# Está basada en la imagen 'image_9b6dc3.png' que proporcionaste.
SALON_CONTEXT = """
Eres un asistente virtual amable y servicial de la "Peluquería Brillo Estelar".
Tu única tarea es responder preguntas de los clientes basándote ESTRICTAMENTE en la
información que te proporciono a continuación. No inventes servicios, precios u horarios.
Si el usuario pregunta por algo que no está en la lista (ej. "manicura"),
debes responder amablemente que no ofreces ese servicio.

Aquí está la información de la peluquería:

--- INFORMACIÓN DE PELUQUERÍA BRILLO ESTELAR ---

Servicios disponibles:
- Corte de cabello: $15
- Tinte básico: $25
- Tinte premium: $40
- Peinado: $20
- Lavado y secado: $10
- Tratamiento capilar: $30
- Barbería (afeitado y recorte): $18

Horario de atención:
- Lunes a Viernes: 9:00 AM - 7:00 PM
- Sábado: 9:00 AM - 3:00 PM
- Domingo: cerrado

Citas:
- No se necesita cita previa.

--- FIN DE LA INFORMACIÓN ---

Responde de forma concisa y amigable.
"""

# --- 3. Lógica de la Aplicación ---

def enviar_pregunta():
    """
    Toma la pregunta del usuario, la envía a la API de Gemini
    con el contexto del salón y muestra la respuesta.
    """
    user_question = entry_pregunta.get()
    if not user_question:
        return

    # Deshabilitar controles mientras se procesa
    entry_pregunta.config(state='disabled')
    btn_enviar.config(state='disabled')

    # Mostrar la pregunta del usuario en el chat
    mostrar_mensaje(f"Tú: {user_question}\n", "user")

    # Mostrar un mensaje de "pensando"
    mostrar_mensaje("Asistente: Pensando...\n", "assistant")

    # Construir el prompt completo
    full_prompt = f"{SALON_CONTEXT}\n\nPregunta del cliente: {user_question}"

    try:
        # --- 4. Manejo de la Respuesta (JSON) ---
        # La librería 'google-generativeai' maneja el JSON internamente.
        # Al llamar a `generate_content`, envía la petición y recibe un
        # objeto de respuesta complejo (JSON).
        # Nosotros simplemente accedemos a la parte del texto con `response.text`.
        # Este es el "manejo de JSON" del que habla la práctica.
        response = model.generate_content(full_prompt)

        # Extraer el texto de la respuesta
        ai_response = response.text

        # Borrar el mensaje "Pensando..."
        chat_area.config(state='normal')
        # Buscar la última línea (que es "Asistente: Pensando...")
        # 'end-1c' es el final, '-1l' es una línea atrás, 'lineend' es el final de esa línea.
        chat_area.delete("end-2l", "end-1l")
        chat_area.config(state='disabled')

        # Mostrar la respuesta real de la IA
        mostrar_mensaje(f"Asistente: {ai_response.strip()}\n", "assistant")

    except Exception as e:
        # Manejar errores de la API (ej. contenido bloqueado, error de red)
        chat_area.config(state='normal')
        chat_area.delete("end-2l", "end-1l")
        chat_area.config(state='disabled')
        mostrar_mensaje(f"Asistente: Lo siento, tuve un problema al procesar tu solicitud. Error: {e}\n", "error")

    finally:
        # Limpiar la entrada y reactivar controles
        entry_pregunta.delete(0, tk.END)
        entry_pregunta.config(state='normal')
        btn_enviar.config(state='normal')
        # Mover el foco de vuelta al entry
        entry_pregunta.focus_set()

def mostrar_mensaje(message, tag):
    """Añade un mensaje al área de chat con un 'tag' para estilo."""
    chat_area.config(state='normal')
    chat_area.insert(tk.END, message, tag)
    # Hacer autoscroll hasta el final
    chat_area.see(tk.END)
    chat_area.config(state='disabled')

def on_enter_key(event):
    """Permite enviar la pregunta presionando 'Enter'."""
    enviar_pregunta()

# --- 5. Creación de la Interfaz Gráfica (Tkinter) ---

# Ventana principal
root = tk.Tk()
root.title("Asistente de Peluquería")
root.geometry("500x600")

# Frame principal
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Área de chat (ScrolledText para la barra de desplazamiento)
chat_area = scrolledtext.ScrolledText(main_frame,
                                      wrap=tk.WORD,
                                      state='disabled',
                                      font=("Arial", 11))
chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Definir estilos (tags) para el chat
# 'user' se alinea con el ejemplo de la imagen
chat_area.tag_configure("user", font=("Arial", 11, "bold"), foreground="#003366")
chat_area.tag_configure("assistant", font=("Arial", 11), foreground="#000000")
chat_area.tag_configure("info", font=("Arial", 10, "italic"), foreground="#555555")
chat_area.tag_configure("error", font=("Arial", 11, "bold"), foreground="#FF0000")

# Frame inferior para la entrada y el botón
bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

# Cuadro de entrada de texto
entry_pregunta = tk.Entry(bottom_frame, font=("Arial", 11), width=40)
entry_pregunta.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
# Vincular la tecla 'Enter' a la función de enviar
entry_pregunta.bind("<Return>", on_enter_key)

# Botón de Enviar
btn_enviar = tk.Button(bottom_frame,
                       text="Enviar",
                       command=enviar_pregunta,
                       font=("Arial", 10, "bold"),
                       bg="#0078D4",
                       fg="white",
                       relief=tk.FLAT,
                       padx=10)
btn_enviar.pack(side=tk.RIGHT, padx=(0, 5))

# Mensaje de bienvenida
mostrar_mensaje("Bienvenido al Asistente de Peluquería Brillo Estelar ✨\n", "assistant")
mostrar_mensaje("Escribe tu pregunta abajo y presiona 'Enviar'.\n\n", "info")

# Iniciar el bucle principal de la aplicación
root.mainloop()