from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.adminService import AdminService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies

adminBp = Blueprint("admin", __name__)

@adminBp.route("/")
def index():
    return render_template("login.html")

@adminBp.route("/adminLogin", methods=["POST"])
def adminLogin():
    mail = request.form.get("adminMail")
    sifre = request.form.get("adminSifre")

    admin = AdminService.login(mail, sifre)

    if not admin:
        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("admin.index"))
    
    token = create_access_token(identity=str(admin.id))
    
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
 
@adminBp.route("/logout")
def logout():
    response = redirect(url_for("admin.index"))
    
    session.pop("adminId", None)
    session.pop("adminName", None)
    
    flash("Çıkış yaptınız.", "info")
    return response