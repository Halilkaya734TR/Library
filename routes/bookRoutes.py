from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from repository.adminLogRepository import AdminLogRepository
from repository.adminRepository import AdminRepository
from datetime import datetime
from services.bookService import BookService
from services.borrowService import BorrowService
from repository.loanRepository import LoanRepository
from services.delayFineService import delayFineService



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
    
    activeFineCount = delayFineService.countActiveFine(memberID)
    if activeFineCount > 0:
        return jsonify({"error": "Aktif cezanız bulunduğu için ödünç alma işlemi yapılamaz!"}), 403
    
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
    data = request.get_json()
    BookService.addBook(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 7, datetime.now(), {"bookName": data.get("bookName")})
    except Exception:
        pass

    return jsonify({"message": "Kitap başarıyla eklendi!"})

@bookBp.route("/kitapDuzenleme", methods=["POST"])
@jwt_required()
def kitapDuzenleme():
    data = request.get_json()
    BookService.editBook(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 8, datetime.now(), {"bookID": data.get("bookID"), "bookName": data.get("bookName")})
    except Exception:
        pass

    return jsonify({"message": "Seçilen kitap başarıyla düzenlendi!"})

@bookBp.route("/kitapSilme", methods=["POST"])
@jwt_required()
def kitapSilme():
    try:
        ids = request.get_json()["ids"]
        BookService.deleteBooks(ids)
        try:
            admin_id = get_jwt_identity()
            admin = AdminRepository.getAdminById(admin_id)
            AdminLogRepository.saveParams(admin_id, admin.name, 9, datetime.now(), {"deletedIDs": ids})
        except Exception:
            pass

        return jsonify({"message": "Kitaplar silindi"})
    except Exception:
        return jsonify({"error": "Ödünç alınmış kitap silinemez"}), 400
    