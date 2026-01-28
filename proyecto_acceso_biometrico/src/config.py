import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Clase encargada ÚNICAMENTE de servir las credenciales.
    No realiza conexiones.
    """
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')