from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.adminService import AdminService
from repository.adminRepository import AdminRepository
from flask import jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, set_access_cookies

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
    adminID = session.get("adminID")
    admin = None
    if adminID:
        adminObj = AdminRepository.getAdminById(adminID)
        if adminObj:
            admin = {"username": adminObj.name, "email": adminObj.mail}
    return render_template("adminInfo.html", admin=admin)


@adminBp.route('/adminProfilGuncelle', methods=['POST'])
@jwt_required()
def adminProfilGuncelle():
    data = request.get_json()
    adminId = session.get('adminId')
    if not adminId:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    username = data.get('username')
    email = data.get('email')
    AdminRepository.updateAdmin(adminId, username, email)
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

    ok, msg = AdminRepository.changePassword(adminId, old_password, new_password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400

    return jsonify({"success": True, "message": msg})


@adminBp.route('/adminSil', methods=['POST'])
@jwt_required()
def adminSil():
    data = request.get_json()
    adminId = session.get('adminId')
    if not adminId:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    password = data.get('password')
    ok, msg = AdminRepository.deleteAdmin(adminId, password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400

    response = redirect(url_for('admin.index'))
    unset_jwt_cookies(response)
    session.pop('adminId', None)
    session.pop('adminName', None)
    return jsonify({"success": True, "message": msg})
 
@adminBp.route("/logout")
def logout():
    response = redirect(url_for("admin.index"))
    unset_jwt_cookies(response)
    
    session.pop("adminId", None)
    session.pop("adminName", None)
    
    flash("Çıkış yaptınız.", "info")
    return response