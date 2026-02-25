import tkinter as tk
from tkinter import messagebox, scrolledtext
from src.voice_service import VoiceService
from src.auth_dao import AuthDAO


class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit Login")
        self.root.geometry("500x500")

        self.voice_service = VoiceService()

        # UI Elements
        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5)

        tk.Button(root, text="1. Registrar por Voz", command=self.registrar, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(root, text="2. Login por Voz", command=self.login, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(root, text="3. Panel de Auditoría Crítica", command=self.auditoria, bg="#f44336", fg="white").pack(
            pady=10)

        self.text_area = scrolledtext.ScrolledText(root, width=50, height=10)
        self.text_area.pack(pady=10)

    def registrar(self):
        usuario = self.entry_user.get()
        if not usuario:
            messagebox.showwarning("Aviso", "Introduce un usuario primero")
            return

        messagebox.showinfo("Micrófono", "Pulsa Aceptar y di tu frase secreta.")
        resultado = self.voice_service.capturar_y_reconocer()  # Uso del Facade [cite: 101]

        if resultado["status"] == "OK":
            frase = resultado["texto"]
            # Confirmación de la frase [cite: 102]
            if messagebox.askyesno("Confirmar", f"¿Tu frase secreta es: '{frase}'?"):
                if AuthDAO.registrar_usuario(usuario, frase):
                    messagebox.showinfo("Éxito", "Usuario registrado.")
                else:
                    messagebox.showerror("Error", "El usuario ya existe o hubo un error.")
        else:
            messagebox.showerror("Error de Audio", resultado.get("motivo", "Desconocido"))

    def login(self):
        usuario = self.entry_user.get()
        user_data = AuthDAO.obtener_usuario(usuario)

        if not user_data:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        user_id, passphrase_guardada, intentos = user_data

        messagebox.showinfo("Micrófono", "Pulsa Aceptar y di tu frase secreta para entrar.")
        resultado = self.voice_service.capturar_y_reconocer()  # Uso del Facade [cite: 114]

        if resultado["status"] == "OK":
            frase_dicha = resultado["texto"]

            if frase_dicha == passphrase_guardada:
                # Éxito: Guardar latencia y confianza [cite: 117]
                log_data = {"status": "OK", "confianza": resultado["confianza"], "latencia": resultado["latencia"]}
                AuthDAO.registrar_log(user_id, log_data)
                messagebox.showinfo("Acceso", "¡Acceso concedido!")
            else:
                # Fallo: Registrar intentos restantes [cite: 115]
                intentos_restantes = 2 - intentos  # Suponiendo un máximo de 3
                log_data = {"status": "FAIL", "frase_intentada": frase_dicha, "intentos_restantes": intentos_restantes}
                AuthDAO.registrar_log(user_id, log_data)
                messagebox.showerror("Acceso Denegado", "Frase incorrecta.")
        else:
            # Error técnico [cite: 111]
            log_data = {"status": "ERROR", "motivo": resultado.get("motivo")}
            AuthDAO.registrar_log(user_id, log_data)
            messagebox.showerror("Error", "No se pudo procesar el audio.")

    def auditoria(self):
        self.text_area.delete(1.0, tk.END)
        resultados = AuthDAO.auditoria_critica()  # Ejecuta la consulta profunda JSONB [cite: 124]

        self.text_area.insert(tk.END, "--- REGISTROS CRÍTICOS ---\n\n")
        for r in resultados:
            self.text_area.insert(tk.END, f"Usuario: {r[0]} | Estado: {r[1]} | Confianza: {r[2]}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()