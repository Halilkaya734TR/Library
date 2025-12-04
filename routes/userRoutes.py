from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.userService import UserService
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, set_access_cookies


userBp = Blueprint("user", __name__)

@userBp.route("/")
def index():
    return render_template("login.html")

@userBp.route("/userLogin", methods=["POST"])
def userLogin():
    mail = request.form.get("mail")
    sifre = request.form.get("sifre")

    user = UserService.login(mail, sifre)

    if not user:
        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("user.index"))
    
    token = create_access_token(identity=str(user.id))
    session["userId"] = user.id
    session["userName"] = user.name
    
    response = redirect(url_for("user.member"))
    set_access_cookies(response, token)
    
    flash("Giriş Başarılı!", "success")
    return response

@userBp.route("/member")
@jwt_required()
def member():
    return render_template("member.html")

@userBp.route("/kitaplar-sayfasi")
@jwt_required()
def kitaplarSayfasi():
    return render_template("kitaplar.html")

@userBp.route("/register", methods=["POST"])
def register():
    name = request.form.get("yeniKullanici")
    email = request.form.get("email")
    sifre= request.form.get("yeniSifre")

    sonuc = UserService.register(name, email, sifre)
    if sonuc == "Mail Var":
        flash("Bu mail zaten kayıtlı!", "danger")
        return redirect(url_for("user.index"))
    
    flash("Kayıt başarılı! Giriş yapabilirsiniz!", "success")
    return redirect(url_for("user.index"))


@userBp.route("/logout")
def logout():
    response = redirect(url_for("user.index"))
    unset_jwt_cookies(response)
    
    session.pop("userId", None)
    session.pop("userName", None)

    flash("Çıkış yaptınız.", "info")
    return response