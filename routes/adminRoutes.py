from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.adminService import AdminService

adminBp = Blueprint("admin", __name__)

@adminBp.route("/")
def index():
    return render_template("login.html")

@adminBp.route("/adminLogin", methods=["POST"])
def adminLogin():
    mail = request.form.get("adminMail")
    sifre = request.form.get("adminSifre")

    admin = AdminService.login(mail, sifre)

    if admin:
        session["adminId"] = admin.id
        session["adminName"] = admin.name
        flash("Giriş Başarılı!", "success")
        return redirect(url_for("admin.admin"))
    else:
        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("admin.index"))
    
@adminBp.route("/admin")
def admin():
    if "adminId" in session:
        return render_template("admin.html")
    
    flash("Önce giriş yapmalısınız!", "danger")
    return redirect(url_for("admin.index"))



@adminBp.route("/logout")
def logout():
    session.pop("adminId", None)
    session.pop("adminName", None)
    flash("Çıkış yaptınız.", "info")
    return redirect(url_for("admin.index"))