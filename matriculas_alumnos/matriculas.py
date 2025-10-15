import os
import json
from io import open
RUTA_ARCHIVO = "alumnos_matriculados.json"

def _cargar_nombres() -> list[str]:
    """Carga la lista de nombres de alumnos desde el archivo JSON."""
    if not os.path.exists(RUTA_ARCHIVO):
        return []
        
    try:
        with open(RUTA_ARCHIVO, 'r', encoding='utf-8') as f:
            nombres = json.load(f)
            return nombres if isinstance(nombres, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _guardar_nombres(nombres: list[str]):
    """Guarda la lista de nombres de alumnos en el archivo JSON."""
    with open(RUTA_ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(nombres, f, indent=4)


def matricular_alumno():
    """Opción 1: Matricular alumno."""
    nombre = input("Introduce el nombre del alumno a matricular: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
        
    nombres = _cargar_nombres()
    
    if nombre.lower() in [n.lower() for n in nombres]:
        print(f"Aviso: El alumno '{nombre}' ya estaba matriculado.")
        return

    nombres.append(nombre)
    _guardar_nombres(nombres)
    print(f"Éxito: Alumno '{nombre}' matriculado correctamente.")

def listar_alumnos():
    """Opción 2: Listar alumnos."""
    nombres = _cargar_nombres()
    
    if not nombres:
        print("No hay alumnos matriculados.")
        return

    print("\n--- Lista de Alumnos Matriculados ---")
    for i, nombre in enumerate(nombres, 1):
        print(f"{i}. Nombre: {nombre}")
    print("-" * 37)

def eliminar_archivo_alumnos():
    """Opción 3: Eliminar archivo de alumnos."""
    confirmacion = input("¿Estás seguro de que deseas eliminar el archivo de alumnos? (s/N): ").lower()
    if confirmacion == 's':
        if os.path.exists(RUTA_ARCHIVO):
            os.remove(RUTA_ARCHIVO)
            print("Éxito: Archivo de alumnos eliminado correctamente.")
        else:
            print("Aviso: El archivo de alumnos no existía para ser eliminado.")
    else:
        print("Operación cancelada.")

def mostrar_menu():
    print("\n--- Gestión de Matrículas de Alumnos ---")
    print("1) Matricular alumno")
    print("2) Listar alumnos")
    print("3) Eliminar archivo de alumnos")
    print("4) Salir")
    print("-" * 38)

def main():
    while True:
        mostrar_menu()
        try:
            opcion = input("Selecciona una opción (1-4): ")
            if opcion == '1':
                matricular_alumno()
            elif opcion == '2':
                listar_alumnos()
            elif opcion == '3':
                eliminar_archivo_alumnos()
            elif opcion == '4':
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Por favor, introduce un número del 1 al 4.")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado. {e}")

if __name__ == '__main__':
    main()