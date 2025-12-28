from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.adminService import AdminService
from services.userService import UserService
from datetime import datetime, date
from repository.userLogRepository import UserLogRepository
from repository.adminLogRepository import AdminLogRepository
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, set_access_cookies, get_jwt_identity
from datetime import datetime

adminBp = Blueprint("admin", __name__)

@adminBp.route("/")
def index():
    return render_template("login.html")

@adminBp.route("/adminLogin", methods=["POST"])
def adminLogin():
    mail = request.form.get("adminMail") or request.args.get("adminMail")
    sifre = request.form.get("adminSifre") or request.args.get("adminSifre")

    admin = AdminService.login(mail, sifre)

    if not admin:
        if request.accept_mimetypes.best == "application/json":
            return jsonify(
                success=False,
                message="Girilen bilgiler uyuşmuyor!"
            ), 401

        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("admin.index"))

    token = create_access_token(
        identity=str(admin.id),
        additional_claims={"role": "admin"}
    )

    if request.accept_mimetypes.best == "application/json":
        response = jsonify(
            success=True,
            message="Admin girişi başarılı",
            admin={
                "id": admin.id,
                "name": admin.name
            }
        )
        set_access_cookies(response, token)
        return response

    session["adminId"] = admin.id
    session["adminName"] = admin.name

    response = redirect(url_for("admin.admin"))
    set_access_cookies(response, token)

    flash("Giriş Başarılı!", "success")
    return response

@adminBp.route("/admin")
@jwt_required()
def admin():
    return render_template("admin.html", admin=session.get("adminName"))

@adminBp.route("/kitapİslemler")
@jwt_required()
def kitapİslemler():
    return render_template("kitapİslemler.html")

@adminBp.route("/yazarlar")
@jwt_required()
def yazarlar():
    return render_template("yazarlar.html")

@adminBp.route("/kategoriler")
@jwt_required()
def kategoriler():
    return render_template("kategoriler.html")

@adminBp.route("/yayinevi")
@jwt_required()
def yayinevi():
    return render_template("yayinevi.html")

@adminBp.route("/adminInfo")
@jwt_required()
def adminInfo():
    admins = AdminService.getAllAdmins()
    return render_template("adminInfo.html", admins=admins)

@adminBp.route("/adminInfo/veri")
@jwt_required()
def getAdminInfo():
    adminId = get_jwt_identity()
    if not adminId:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401
    
    admin = AdminService.getAdminByID(adminId)
    if not admin:
        return jsonify({"success": False, "message": "Admin bulunamadı"}), 404
    
    return jsonify({"success": True, "data": {
        "id": admin.id,
        "username": admin.name,
        "email": admin.mail
    }})

@adminBp.route('/adminProfilGuncelle', methods=['POST'])
@jwt_required()
def adminProfilGuncelle():
    data = request.get_json()
    adminId = get_jwt_identity()
    if not adminId:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    username = data.get('username')
    email = data.get('email')
    AdminService.updateAdmin(adminId, username, email)
    session['adminName'] = username
    return jsonify({"success": True, "message": "Profil güncellendi"})


@adminBp.route('/adminSifreDegistir', methods=['POST'])
@jwt_required()
def adminSifreDegistir():
    data = request.get_json()
    adminId = session.get('adminId')
    if not adminId:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    new_password_confirm = data.get('new_password_confirm')
    if new_password != new_password_confirm:
        return jsonify({"success": False, "message": "Yeni şifreler eşleşmiyor"}), 400

    ok, msg = AdminService.changePassword(adminId, old_password, new_password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400

    return jsonify({"success": True, "message": msg})


@adminBp.route('/adminSil', methods=['POST'])
@jwt_required()
def adminSil():
    data = request.get_json()
    adminId = get_jwt_identity()
    if not adminId:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    password = data.get('password')
    ok, msg = AdminService.deleteAdmin(adminId, password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400

    response = redirect(url_for('admin.index'))
    unset_jwt_cookies(response)
    session.pop('adminId', None)
    session.pop('adminName', None)
    return jsonify({"success": True, "message": msg})

@adminBp.route("/loglar")
@jwt_required()
def loglar():
    return render_template("loglar.html")

@adminBp.route("/admin/userLogs")
@jwt_required()
def getAllUserLogs():
    rows = UserLogRepository.getAllLogs()
    
    def fmt(d):
        if isinstance(d, datetime):
            return d.strftime("%d.%m.%Y %H:%M:%S")
        if isinstance(d, date):
            return d.strftime("%d.%m.%Y")
        return str(d) if d is not None else ""
    
    for row in rows:
        if "logDate" in row:
            row["logDate"] = fmt(row["logDate"])
    
    return jsonify(rows)

@adminBp.route("/admin/adminLogs")
@jwt_required()
def getAllAdminLogs():
    rows = AdminLogRepository.getAllLogs()
    
    def fmt(d):
        if isinstance(d, datetime):
            return d.strftime("%d.%m.%Y %H:%M:%S")
        if isinstance(d, date):
            return d.strftime("%d.%m.%Y")
        return str(d) if d is not None else ""
    
    for row in rows:
        if "logDate" in row:
            row["logDate"] = fmt(row["logDate"])
    
    return jsonify(rows)

@adminBp.route("/admin/cezalar")
@jwt_required()
def cezalar():
    return render_template("cezalar.html")

@adminBp.route("/kullanicilar")
@jwt_required()
def kullanicilar():
    return render_template("kullanicilar.html")

@adminBp.route("/admin/kullanicilar")
@jwt_required()
def getAllUsers():
    return jsonify(UserService.getAllUsers())

@adminBp.route("/admin/kullaniciDurum", methods=["POST"])
@jwt_required()
def changeStatus():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Veri yok"}), 400

    memberID = data.get("memberID")
    status = data.get("status")

    if memberID is None or status is None:
        return jsonify({"success": False, "message": "Eksik veri"}), 400

    UserService.updateUserStatus(memberID, status)

    return jsonify({
        "success": True,
        "message": "Kullanıcı durumu güncellendi"
    })

@adminBp.route("/logout")
def logout():
    response = redirect(url_for("admin.index"))
    unset_jwt_cookies(response)
    
    session.pop("adminId", None)
    session.pop("adminName", None)
    
    flash("Çıkış yaptınız.", "info")
    return response

@adminBp.route("/adminler")
@jwt_required()
def adminler():
    try:
        current_id = get_jwt_identity()
        current_id = int(current_id) if current_id is not None else None
    except Exception:
        current_id = None
    return render_template("adminler.html", currentAdminId=current_id)

@adminBp.route("/admin/adminler-veri")
@jwt_required()
def adminlerVeri():
    admins = AdminService.getAllAdmins()
    return jsonify(admins)

@adminBp.route("/admin/adminEkle", methods=["POST"])
@jwt_required()
def adminEkle():
    data = request.get_json()
    name = data.get("adminName", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    ok, msg = AdminService.addAdmin(name, email, password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400
    
    admin_id = get_jwt_identity()
    admin = AdminService.getAdminById(admin_id)
    AdminLogRepository.saveParams(admin_id, admin.name, 22, datetime.now(), {"adminName": name})
    
    return jsonify({"success": True, "message": msg})

@adminBp.route("/admin/adminSil", methods=["POST"])
@jwt_required()
def DeleteAdmin():
    data = request.get_json()
    silinecekAdminId = data.get("adminID")
    try:
        silinecekAdminId = int(silinecekAdminId)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Geçersiz admin ID"}), 400

    if silinecekAdminId == 1:
        return jsonify({"success": False, "message": "Varsayılan admin silinemez"}), 403

    try:
        current_admin_id = get_jwt_identity()
        current_admin_id = int(current_admin_id) if current_admin_id is not None else None
    except Exception:
        current_admin_id = None

    if current_admin_id is not None and silinecekAdminId == current_admin_id:
        return jsonify({"success": False, "message": "Kendi hesabınızı silemezsiniz"}), 403
    
    admin = AdminService.getAdminById(silinecekAdminId)
    if not admin:
        return jsonify({"success": False, "message": "Admin bulunamadı"}), 404

    ok, msg = AdminService.deleteAdminById(silinecekAdminId)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400
    
    admin_id = get_jwt_identity()
    current_admin = AdminService.getAdminById(admin_id)
    AdminLogRepository.saveParams(admin_id, current_admin.name, 21, datetime.now(), {"adminName": admin.name})
    
    return jsonify({"success": True, "message": msg})