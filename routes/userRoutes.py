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

@userBp.route("/logout")
def logout():
    session.pop("userId", None)
    session.pop("userName", None)
    flash("Çıkış yaptınız.", "info")
    return redirect(url_for("user.index"))