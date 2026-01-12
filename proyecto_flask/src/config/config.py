import os

class Config:
    # Define la base de datos sqlite
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///library.db')