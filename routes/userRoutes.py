from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from services.userService import UserService
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, set_access_cookies


userBp = Blueprint("user", __name__)

@userBp.route("/")
def index():
    return render_template("login.html")

@userBp.route("/userLogin", methods=["POST"])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")

    user = UserService.login(email, password)

    if not user:
        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("user.index"))
    
    token = create_access_token(identity=str(user.memberID))
    session["userId"] = user.memberID
    session["userName"] = user.username
    
    response = redirect(url_for("user.member"))
    set_access_cookies(response, token)
    
    flash("Giriş Başarılı!", "success")
    return response

@userBp.route("/member")
@jwt_required()
def member():
    return render_template("member.html", username=session.get("userName"))

@userBp.route("/kitaplar-sayfasi")
@jwt_required()
def kitaplarSayfasi():
    return render_template("kitaplar.html")

@userBp.route("/kitaplarim")
@jwt_required()
def kitaplarim():
    return render_template("kitaplarim.html")

@userBp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password= request.form.get("password")

    sonuc = UserService.register(username, email, password)
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