import psycopg2
from src.config import Config


class DBConnection:
    """
    Patrón Singleton: Garantiza una única conexión a la BBDD.
    """
    _connection = None  # Variable de clase para almacenar la instancia única

    @classmethod
    def get_connection(cls):
        # 1. Verificamos si ya existe una conexión y si está abierta (no es None y no está cerrada)
        if cls._connection is not None and cls._connection.closed == 0:
            return cls._connection

        # 2. Si no existe o se cerró, creamos una nueva
        try:
            print("--- Creando NUEVA conexión a la Base de Datos ---")
            cls._connection = psycopg2.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT
            )
            return cls._connection
        except Exception as e:
            print(f"Error al conectar: {e}")
            return None