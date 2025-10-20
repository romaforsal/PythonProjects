import json
import os
from io import open
from ..dominio.alumno import Alumno

class AlumnosMatriculados:
    """
    Realiza las operaciones sobre el fichero de alumnos matriculados.
    Todos los métodos son estáticos.
    """
    _ruta_archivo: str = "proyecto_matriculas/alumnos_matriculados.json"
    
    @staticmethod
    def _cargar_alumnos() -> list[Alumno]:
        """Carga la lista de alumnos desde el archivo."""
        if not os.path.exists(AlumnosMatriculados._ruta_archivo):
            return []
            
        try:
            with open(AlumnosMatriculados._ruta_archivo, 'r', encoding='utf-8') as f:
                nombres = json.load(f)
                return [Alumno(nombre) for nombre in nombres]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @staticmethod
    def _guardar_alumnos(alumnos: list[Alumno]):
        """Guarda la lista de alumnos en el archivo."""
        nombres = [alumno.nombre for alumno in alumnos]
        
        with open(AlumnosMatriculados._ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(nombres, f, indent=4)

    
    @staticmethod
    def matricular_alumno(alumno: Alumno) -> bool:
        """Añade un alumno al fichero si no existe ya[cite: 484]."""
        alumnos = AlumnosMatriculados._cargar_alumnos()

        if alumno in alumnos:
            return False

        alumnos.append(alumno)
        AlumnosMatriculados._guardar_alumnos(alumnos)
        return True

    @staticmethod
    def listar_alumnos() -> list[Alumno]:
        """Devuelve la lista de todos los alumnos matriculados[cite: 485]."""
        return AlumnosMatriculados._cargar_alumnos()

    @staticmethod
    def eliminar_alumnos() -> bool:
        """Elimina el archivo de alumnos[cite: 486]."""
        if os.path.exists(AlumnosMatriculados._ruta_archivo):
            os.remove(AlumnosMatriculados._ruta_archivo)
            return True
        return False