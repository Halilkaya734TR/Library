from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.authorService import AuthorService

authorBp = Blueprint("author", __name__)

@authorBp.route("/admin/yazarlar")
@jwt_required()
def adminYazarlar():
    authors = AuthorService.getAuthors()
    return jsonify([{"authorID": a.authorID, "authorName": a.authorName} for a in authors])

@authorBp.route("/yazarEkle", methods=["POST"])
@jwt_required()
def yazarEkle():
    data = request.get_json()
    AuthorService.addAuthor(data)
    return jsonify({"message": "Yazar eklendi"})

@authorBp.route("/yazarDuzenleme", methods=["POST"])
@jwt_required()
def yazarDuzenleme():
    data = request.get_json()
    AuthorService.editAuthor(data)
    return jsonify({"message": "Yazar güncellendi"})

@authorBp.route("/yazarSilme", methods=["POST"])
@jwt_required()
def yazarSilme():
    ids = request.get_json().get("ids", [])
    try:
        AuthorService.deleteAuthors(ids)
        return jsonify({"message": "Yazarlar silindi"})
    except Exception as ex:
        msg = str(ex)
        if msg.startswith("linked:"):
            aid = msg.split(":",1)[1]
            return jsonify({"error": f"Yazar (id={aid}) en az 1 kitaba ait olduğu için silinemez."}), 400
        return jsonify({"error": "Silme sırasında hata oluştu."}), 500
