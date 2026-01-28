from src.conexion_db import DBConnection
import psycopg2


class UsuarioDAO:
    """
    Data Access Object: Gestiona el CRUD de la tabla usuarios.
    """

    @staticmethod
    def registrar_usuario(nombre, foto_bytes):
        conn = DBConnection.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios (nombre, foto_blob) VALUES (%s, %s)"
            # psycopg2 maneja bytes directamente como BYTEA
            cursor.execute(query, (nombre, foto_bytes))
            conn.commit()
            cursor.close()
            print(f"Usuario {nombre} registrado con éxito (BLOB guardado).")
            return True
        except Exception as e:
            print(f"Error en DAO: {e}")
            conn.rollback()
            return False

    @staticmethod
    def obtener_todos():
        """Recupera todos los usuarios para el entrenamiento"""
        conn = DBConnection.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, foto_blob FROM usuarios")
            filas = cursor.fetchall()
            cursor.close()
            return filas  # Devuelve lista de tuplas (id, nombre, bytes)
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
            return []