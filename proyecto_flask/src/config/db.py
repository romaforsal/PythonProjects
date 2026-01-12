from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.config import Config

# Crear el motor de la base de datos
engine = create_engine(Config.DATABASE_URI)

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

# Crear la clase base para los modelos
Base = declarative_base()