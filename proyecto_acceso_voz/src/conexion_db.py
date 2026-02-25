import psycopg2
from src.config import Config

class DBConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is not None and cls._connection.closed == 0:
            return cls._connection
        try:
            cls._connection = psycopg2.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT
            )
            return cls._connection
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None