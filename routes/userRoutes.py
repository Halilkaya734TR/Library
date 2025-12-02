from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.userService import UserService

userBp = Blueprint("user", __name__)

@userBp.route("/")
def index():
    return render_template("login.html")

@userBp.route("/userLogin", methods=["POST"])
def userLogin():
    mail = request.form.get("mail")
    sifre = request.form.get("sifre")

    user = UserService.login(mail, sifre)

    if user:
        session["userId"] = user.id
        session["userName"] = user.name
        flash("Giriş Başarılı!", "success")
        return redirect(url_for("user.member"))
    else:
        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("user.index"))
    
@userBp.route("/member")
def member():
    if "userId" in session:
        return render_template("member.html")
    
    flash("Önce giriş yapmalısınız!", "danger")
    return redirect(url_for("user.index"))

@userBp.route("/kitaplar-sayfasi") 
def kitaplarSayfasi():
    if "userId" not in session:
        flash("Önce giriş yapmalısınız!", "danger")
        return redirect(url_for("user.index"))
        
    return render_template("kitaplar.html")

@userBp.route("/register", methods=["POST"])
def register():
    name = request.form.get("yeniKullanici")
    email = request.form.get("email")
    sifre= request.form.get("yeniSifre")

    sonuc = UserService.register(name, email, sifre)
    if sonuc == "Mail Var":
        flash("Bu mail zaten kayıtlı!", "danger")
        return redirect(url_for("admin.index"))
    
    flash("Kayıt başarılı! Giriş yapabilirsiniz!", "success")
    return redirect(url_for("admin.index"))


@userBp.route("/logout")
def logout():
    session.pop("userId", None)
    session.pop("userName", None)
    flash("Çıkış yaptınız.", "info")
    return redirect(url_for("user.index"))