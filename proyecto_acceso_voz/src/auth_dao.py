from src.conexion_db import DBConnection
import json


class AuthDAO:

    @staticmethod
    def registrar_usuario(username, passphrase):
        conn = DBConnection.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios_voz (username, passphrase) VALUES (%s, %s) RETURNING id",
                (username, passphrase)
            )
            usuario_id = cursor.fetchone()[0]

            # Registro de auditoría inicial (Éxito) [cite: 104, 107]
            log_data = {"status": "OK", "confianza": 0.98, "latencia": "1.2s"}
            cursor.execute(
                "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                (usuario_id, json.dumps(log_data))
            )

            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error registrando usuario: {e}")
            conn.rollback()
            return False

    @staticmethod
    def obtener_usuario(username):
        conn = DBConnection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, passphrase, intentos_fallidos FROM usuarios_voz WHERE username = %s",
                           (username,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except:
            return None

    @staticmethod
    def registrar_log(usuario_id, log_dict):
        """Inserta datos dinámicos en la bolsa JSONB."""
        conn = DBConnection.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                (usuario_id, json.dumps(log_dict))
            )
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error guardando log: {e}")

    @staticmethod
    def auditoria_critica():
        """Bucea en el JSONB para buscar fallos o baja confianza."""
        conn = DBConnection.get_connection()
        try:
            cursor = conn.cursor()
            # Consulta exacta proporcionada en la práctica [cite: 125-127]
            query = """
                SELECT u.username, l.resultado_json->>'status', l.resultado_json->>'confianza'
                FROM log_accesos_voz l
                JOIN usuarios_voz u ON l.usuario_id = u.id
                WHERE l.resultado_json->>'status' = 'FAIL'
                OR (l.resultado_json->>'confianza')::float < 0.6;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print(f"Error de auditoría: {e}")
            return []