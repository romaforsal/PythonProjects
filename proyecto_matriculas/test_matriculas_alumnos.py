from matriculas_alumnos.dominio.alumno import Alumno
from matriculas_alumnos.servicio.alumnos_matriculados import AlumnosMatriculados

class TestMatriculasAlumnos:
    """
    Contiene un menú con 4 opciones para interactuar con la gestión de matrículas[cite: 491].
    """
    @staticmethod
    def mostrar_menu():
        print("\n--- Gestión de Matrículas de Alumnos ---")
        print("1) Matricular alumno [cite: 492]")
        print("2) Listar alumnos [cite: 493]")
        print("3) Eliminar archivo de alumnos [cite: 494]")
        print("4) Salir [cite: 495]")
        print("-" * 38)

    @staticmethod
    def opcion_matricular_alumno():
        """Opción 1: Matricular alumno[cite: 492]."""
        nombre = input("Introduce el nombre del alumno a matricular: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            return
            
        alumno = Alumno(nombre)
        if AlumnosMatriculados.matricular_alumno(alumno):
            print(f"Éxito: Alumno '{nombre}' matriculado correctamente.")
        else:
            print(f"Aviso: El alumno '{nombre}' ya estaba matriculado.")

    @staticmethod
    def opcion_listar_alumnos():
        """Opción 2: Listar alumnos[cite: 493]."""
        alumnos = AlumnosMatriculados.listar_alumnos()      
        if not alumnos:
            print("No hay alumnos matriculados.")
            return

        print("\n--- Lista de Alumnos Matriculados ---")
        for i, alumno in enumerate(alumnos, 1):
            print(f"{i}. {alumno}")
        print("-" * 37)

    @staticmethod
    def opcion_eliminar_archivo():
        """Opción 3: Eliminar archivo de alumnos[cite: 494]."""
        confirmacion = input("¿Estás seguro de que deseas eliminar el archivo de alumnos? (s/N): ").lower()
        if confirmacion == 's':
            if AlumnosMatriculados.eliminar_alumnos():
                print("Éxito: Archivo de alumnos eliminado correctamente.")
            else:
                print("Aviso: El archivo de alumnos no existía para ser eliminado.")
        else:
            print("Operación cancelada.")

    @staticmethod
    def main():
        while True:
            TestMatriculasAlumnos.mostrar_menu()
            try:
                opcion = input("Selecciona una opción (1-4): ")
                if opcion == '1':
                    TestMatriculasAlumnos.opcion_matricular_alumno()
                elif opcion == '2':
                    TestMatriculasAlumnos.opcion_listar_alumnos()
                elif opcion == '3':
                    TestMatriculasAlumnos.opcion_eliminar_archivo()
                elif opcion == '4':
                    print("Saliendo del programa. ¡Hasta pronto!")
                    break
                else:
                    print("Opción no válida. Por favor, introduce un número del 1 al 4.")
            except Exception as e:
                print(f"Ha ocurrido un error inesperado: {e}")

if __name__ == '__main__':
    TestMatriculasAlumnos.main()