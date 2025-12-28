from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.delayFineService import delayFineService
from services.borrowService import BorrowService
from datetime import datetime, date
from repository.delayFineRepository import DelayFineRepository

delayFineBp = Blueprint("delayFibe", __name__)

@delayFineBp.route("/cezalarim-veri")
@jwt_required()
def cezalarimVeri():
    memberID = get_jwt_identity()
    fines = delayFineService.getFineByID(memberID)
    
    def fmt(d):
        if isinstance(d, datetime):
            return d.strftime("%d.%m.%Y %H:%M:%S")
        if isinstance(d, date):
            return d.strftime("%d.%m.%Y")
        return str(d) if d is not None else ""
    
    return jsonify([{
        "ID": f.ID,
        "userID": f.userID,
        "bookID": f.bookID,
        "delay": f.delay,
        "sum": f.sum,
        "firstDay": fmt(f.firstDay)
    } for f in fines])

@delayFineBp.route("/cezalar-ode", methods=["POST"])
@jwt_required()
def cezaOde():
    memberID = get_jwt_identity()
    if(BorrowService.getActiveLoan(memberID)):
        return jsonify({"success": False, "message": "İade edilmemiş kitap mevcut!"}), 401
        
    delayFineService.deleteByID(memberID)
    return jsonify({"success": True, "message": "Cezalarınız Ödendi!"})

@delayFineBp.route("/admin/cezalar/veri")
@jwt_required()
def getCezalar():
    fines = delayFineService.getAllFine()
    return jsonify({"success": True, "data": [{
        "ID": f["ID"],
        "userID": f["userID"],
        "bookID": f["bookID"],
        "userName": f["userName"] or "Bilinmeyen",
        "bookName": f["bookName"] or "Bilinmeyen",
        "delay": f["delay"],
        "sum": f["sum"],
        "firstDay": f["firstDay"].strftime("%d.%m.%Y %H:%M") if f["firstDay"] else ""
    } for f in fines]})
 