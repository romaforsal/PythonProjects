class Alumno:
    """
    Representa un objeto alumno[cite: 480].
    """
    def __init__(self, nombre: str):
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        """Retorna el nombre del alumno."""
        return self._nombre

    def __str__(self) -> str:
        """Representación en string del objeto, como requiere el diagrama."""
        return f"Alumno(Nombre: {self._nombre})"

    def __eq__(self, other) -> bool:
        """Permite comparar dos alumnos por su nombre."""
        if isinstance(other, Alumno):
            return self._nombre.lower() == other.nombre.lower()
        return False
        
    def __hash__(self):
        """Permite usar objetos Alumno en conjuntos o como claves de diccionario."""
        return hash(self._nombre.lower())