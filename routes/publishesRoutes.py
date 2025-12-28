from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.publisherService import PublisherService
from repository.adminLogRepository import AdminLogRepository
from repository.adminRepository import AdminRepository
from datetime import datetime

publisherBp = Blueprint("publisher", __name__)

@publisherBp.route("/admin/yayinevleri")
@jwt_required()
def adminYayinevleri():
    publisher = PublisherService.getPublishers()
    return jsonify([{"publisherID": p.publisherID, "publisherName": p.publisherName} for p in publisher])

@publisherBp.route("/yayineviEkle", methods=["POST"])
@jwt_required()
def kategoriEkle():
    data = request.get_json()
    PublisherService.addPublisher(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id)
        AdminLogRepository.saveParams(admin_id, admin.name, 16, datetime.now(), {"publisherName": data.get("publisherName")})
    except Exception:
        pass
    return jsonify({"message": "Yayınevi eklendi"})

@publisherBp.route("/yayineviDuzenleme", methods=["POST"])
@jwt_required()
def yayineviDuzenleme():
    data = request.get_json()
    PublisherService.editPublisher(data)
    try:
        admin_id = get_jwt_identity()
        admin = AdminRepository.getAdminById(admin_id) if admin_id else None
        AdminLogRepository.saveParams(admin_id, admin.name, 17, datetime.now(), {"publisherID": data.get("publisherID"), "publisherName": data.get("publisherName")})
    except Exception:
        pass
    return jsonify({"message": "Yayınevi güncellendi"})

@publisherBp.route("/yayineviSilme", methods=["POST"])
@jwt_required()
def yayineviSilme():
    ids = request.get_json().get("ids", [])
    try:
        PublisherService.deletePublisher(ids)
        try:
            admin_id = get_jwt_identity()
            admin = AdminRepository.getAdminById(admin_id)
            AdminLogRepository.saveParams(admin_id, admin.name, 18, datetime.now(), {"deletedIDs": ids})
        except Exception:
            pass
        return jsonify({"message": "Yayınevleri silindi"})
    except Exception as ex:
        msg = str(ex)
        if msg.startswith("linked:"):
            cid = msg.split(":",1)[1]
            return jsonify({"error": f"Yayınevi (id={cid}) en az 1 kitaba ait olduğu için silinemez."}), 400
        return jsonify({"error": "Silme sırasında hata oluştu."}), 500
