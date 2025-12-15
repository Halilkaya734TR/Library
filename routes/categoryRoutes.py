from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.categoryService import CategoryService

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
    return jsonify({"message": "Kategori eklendi"})

@categoryBp.route("/kategoriDuzenleme", methods=["POST"])
@jwt_required()
def kategoriDuzenleme():
    data = request.get_json()
    CategoryService.editCategory(data)
    return jsonify({"message": "Kategori güncellendi"})

@categoryBp.route("/kategoriSilme", methods=["POST"])
@jwt_required()
def kategoriSilme():
    ids = request.get_json().get("ids", [])
    try:
        CategoryService.deleteCategories(ids)
        return jsonify({"message": "Kategoriler silindi"})
    except Exception as ex:
        msg = str(ex)
        if msg.startswith("linked:"):
            cid = msg.split(":",1)[1]
            return jsonify({"error": f"Kategori (id={cid}) en az 1 kitaba ait olduğu için silinemez."}), 400
        return jsonify({"error": "Silme sırasında hata oluştu."}), 500
