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
            "id": b.id, 
            "ad": b.ad,
            "yazar": b.yazar,
            "yayinevi": b.yayinevi   
        }
        for b in books
    ]
    return jsonify(data)