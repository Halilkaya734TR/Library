from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.categoryService import CategoryService
from repository.adminLogRepository import AdminLogRepository
from repository.adminRepository import AdminRepository
from datetime import datetime

categoryBp = Blueprint("category", __name__)

@categoryBp.route("/admin/kategoriler")
@jwt_required()
def adminKategoriler():
    cats = CategoryService.getCategories()
    return jsonify([{"categoryID": c.categoryID, "categoryName": c.categoryName} for c in cats])

@categoryBp.route("/kategoriEkle", methods=["POST"])
@jwt_required()
def kategoriEkle():
    data = request.get_json()
    CategoryService.addCategory(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 13, datetime.now(), {"categoryName": data.get("categoryName")})
    except Exception:
        pass

    return jsonify({"message": "Kategori eklendi"})

@categoryBp.route("/kategoriDuzenleme", methods=["POST"])
@jwt_required()
def kategoriDuzenleme():
    data = request.get_json()
    CategoryService.editCategory(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 14, datetime.now(), {"categoryID": data.get("categoryID"), "categoryName": data.get("categoryName")})
    except Exception:
        pass

    return jsonify({"message": "Kategori güncellendi"})

@categoryBp.route("/kategoriSilme", methods=["POST"])
@jwt_required()
def kategoriSilme():
    ids = request.get_json().get("ids", [])
    try:
        CategoryService.deleteCategories(ids)
        try:
            admin_id = get_jwt_identity()
            admin = AdminRepository.getAdminById(admin_id)
            AdminLogRepository.saveParams(admin_id, admin.name, 15, datetime.now(), {"deletedIDs": ids})
        except Exception:
            pass

        return jsonify({"message": "Kategoriler silindi"})
    except Exception as ex:
        msg = str(ex)
        if msg.startswith("linked:"):
            cid = msg.split(":",1)[1]
            return jsonify({"error": f"Kategori (id={cid}) en az 1 kitaba ait olduğu için silinemez."}), 400
        return jsonify({"error": "Silme sırasında hata oluştu."}), 500
