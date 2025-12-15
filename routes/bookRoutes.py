from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.bookService import BookService
from services.borrowService import BorrowService
from repository.loanRepository import LoanRepository
from services.authorService import AuthorService
from services.publisherService import PublisherService
from services.categoryService import CategoryService


bookBp = Blueprint("book", __name__)

@bookBp.route("/kitaplar")
@jwt_required()
def kitaplar():  
    books = BookService.getBooks()

    data = [
        {
            "bookID":b.bookID,
            "bookName": b.bookName,
            "authorName": b.authorName,
            "publisher": b.publisherName,
            "categoryName": b.categoryName,
            "stock": b.stock   
        }
        for b in books
    ]
    return jsonify(data)

@bookBp.route("/odunc-al", methods=["POST"])
@jwt_required()
def oduncAl():

    data = request.get_json()
    memberID = get_jwt_identity()
    bookIDs = data.get("bookIDs", [])

    if len(bookIDs) == 0:
        return jsonify({"error": "Kitap seçilmedi."}), 400

    current = LoanRepository.countActiveLoans(memberID)

    if current + len(bookIDs) > 3:
        kalan = 3 - current
        return jsonify({"error": f"Zaten {current} kitabınız var. En fazla {kalan} tane daha alabilirsiniz."}), 400

    for bookID in bookIDs:
        BorrowService.borrowBook(memberID, int(bookID))
        BookService.decreaseStock(int(bookID))

    return jsonify({"message": "Kitaplar başarıyla ödünç alındı!"})

@bookBp.route("/kitaplarim-veri")
@jwt_required()
def kitaplarim_veri():

    memberID = get_jwt_identity()
    kitap = BorrowService.getBorrowedBookDetailed(memberID)

    if not kitap:
        return jsonify([])

    return jsonify(kitap)

@bookBp.route("/iade-et", methods=["POST"])
@jwt_required()
def iadeEt():
    data = request.get_json()
    loanIDs = data.get("loanIDs")
    memberID = get_jwt_identity()

    if not loanIDs:
        return jsonify({"error": "Hiç kitap seçilmedi!"}), 400

    BorrowService.returnBooks(memberID, loanIDs)

    return jsonify({"message": "Seçilen kitaplar başarıyla iade edildi!"}), 200

@bookBp.route("/kitap-sayim")
@jwt_required()
def kitap_sayim():
    memberID = get_jwt_identity()
    count = BorrowService.getActiveLoan(memberID)
    return jsonify({"Kitap Sayısı": count})

@bookBp.route("/kitapEkle", methods=["POST"])
@jwt_required()
def kitapEkle():
    BookService.addBook(request.get_json())
    return jsonify({"message": "Kitap başarıyla eklendi!"})

@bookBp.route("/kitapDuzenleme", methods=["POST"])
@jwt_required()
def kitapDuzenleme():
    BookService.editBook(request.get_json())
    return jsonify({"message": "Seçilen kitap başarıyla düzenlendi!"})

@bookBp.route("/kitapSilme", methods=["POST"])
@jwt_required()
def kitapSilme():
    try:
        BookService.deleteBooks(request.get_json()["ids"])
        return jsonify({"message": "Kitaplar silindi"})
    except Exception:
        return jsonify({"error": "Ödünç alınmış kitap silinemez"}), 400

@bookBp.route("/yayincilar")
@jwt_required()
def yayincilar():
    publishers = PublisherService.getPublishers()
    return jsonify([{
        "publisherID": p.publisherID,
        "publisherName": p.publisherName
    } for p in publishers])
