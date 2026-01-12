from flask import request, jsonify
from src.config.db import session
from src.models.book import Book


def init_api_routes(app):
    # --- CREATE (POST) --- [cite: 103, 207]
    @app.route('/api/book', methods=['POST'])
    def create_book():
        data = request.get_json()
        new_book = Book(
            title=data.get('title'),
            author=data.get('author'),
            year=data.get('year')
        )
        session.add(new_book)
        session.commit()
        return jsonify(new_book.to_dict()), 201

    # --- READ ALL (GET) --- [cite: 100, 181]
    @app.route('/api/books', methods=['GET'])
    def get_books():
        books = session.query(Book).all()
        # Convertimos la lista de objetos a lista de diccionarios
        return jsonify([book.to_dict() for book in books]), 200

    # --- READ ONE (GET by ID) --- [cite: 101, 190]
    @app.route('/api/book/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        book = session.query(Book).filter_by(id=book_id).first()
        if book is None:
            return jsonify({"error": "Not Found"}), 404
        return jsonify(book.to_dict()), 200

    # --- UPDATE (PUT) --- [cite: 104, 215]
    @app.route('/api/book/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        book = session.query(Book).filter_by(id=book_id).first()
        if book is None:
            return jsonify({"error": "Not Found"}), 404

        data = request.get_json()

        # Actualizamos si existe el dato, si no mantenemos el anterior
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year = data.get('year', book.year)

        session.commit()
        return jsonify(book.to_dict()), 200

    # --- DELETE (DELETE) --- [cite: 105, 222]
    @app.route('/api/book/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = session.query(Book).filter_by(id=book_id).first()
        if book is None:
            return jsonify({"error": "Not Found"}), 404

        session.delete(book)
        session.commit()
        return jsonify({"message": "Deleted successfully"}), 204