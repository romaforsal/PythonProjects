from flask import Flask
from src.api.routes import init_api_routes
from src.config import db

app = Flask(__name__)

# Esto crea las tablas en la BBDD basadas en los modelos importados
# Importante importar el modelo para que SQLAlchemy lo detecte antes de crear
from src.models.book import Book
db.Base.metadata.create_all(db.engine)

# Inicializar rutas
init_api_routes(app)

if __name__ == '__main__':
    # Debug=True para ver errores detallados [cite: 240]
    app.run(debug=True)