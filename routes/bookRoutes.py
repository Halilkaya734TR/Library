from flask import Blueprint, jsonify, session
from services.bookService import BookService

bookBp = Blueprint("book", __name__)

@bookBp.route("/kitaplar")
def kitaplar():
    if "userId" not in session:
        return jsonify({"error": "Giriş yapılmalı!"}), 403
    
    books = BookService.getBooks()

    data = [
        {
            "name": b.name,
            "author": b.author,
            "publisher": b.publisher,
            "category": b.category,
            "pageNumber": b.pageNumber   
        }
        for b in books
    ]
    return jsonify(data)