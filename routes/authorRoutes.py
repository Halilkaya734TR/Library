from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.authorService import AuthorService
from repository.adminLogRepository import AdminLogRepository
from repository.adminRepository import AdminRepository
from datetime import datetime

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
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 10, datetime.now(), {"authorName": data.get("authorName")})
    except Exception:
        pass
    return jsonify({"message": "Yazar eklendi"})

@authorBp.route("/yazarDuzenleme", methods=["POST"])
@jwt_required()
def yazarDuzenleme():
    data = request.get_json()
    AuthorService.editAuthor(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 11, datetime.now(), {"authorID": data.get("authorID"), "authorName": data.get("authorName")})
    except Exception:
        pass
    return jsonify({"message": "Yazar güncellendi"})

@authorBp.route("/yazarSilme", methods=["POST"])
@jwt_required()
def yazarSilme():
    ids = request.get_json().get("ids", [])
    try:
        AuthorService.deleteAuthors(ids)
        try:
            admin_id = get_jwt_identity()
            admin = AdminRepository.getAdminById(admin_id) 
            AdminLogRepository.saveParams(admin_id, admin.name, 12, datetime.now(), {"deletedIDs": ids})
        except Exception:
            pass
        return jsonify({"message": "Yazarlar silindi"})
    except Exception as ex:
        msg = str(ex)
        if msg.startswith("linked:"):
            aid = msg.split(":",1)[1]
            return jsonify({"error": f"Yazar (id={aid}) en az 1 kitaba ait olduğu için silinemez."}), 400
        return jsonify({"error": "Silme sırasında hata oluştu."}), 500
