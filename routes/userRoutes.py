from flask import Blueprint, request, session, redirect, url_for, flash, render_template, jsonify
from services.userService import UserService
from repository.userRepository import UserRepository
from repository.userLogRepository import UserLogRepository
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, set_access_cookies, get_jwt_identity


userBp = Blueprint("user", __name__)

@userBp.route("/")
def index():
    return render_template("login.html")

@userBp.route("/userLogin", methods=["POST"])
def userLogin():
    email = request.form.get("email") or request.args.get("email")
    password = request.form.get("password") or request.args.get("password")

    user, error = UserService.login(email, password)

    if not user:
        if request.accept_mimetypes.best == "application/json":
            return jsonify(success=False, msg=error), 401

        flash(error, "danger")
        return redirect(url_for("user.index"))

    token = create_access_token(identity=str(user.memberID))

    if request.accept_mimetypes.best == "application/json":
        response = jsonify(
            success=True,
            message="Giriş başarılı",
            user={
                "id": user.memberID,
                "username": user.username
            }
        )
        set_access_cookies(response, token)
        return response

    response = redirect(url_for("user.member"))
    set_access_cookies(response, token)

    session["userID"] = user.memberID
    session["userName"] = user.username

    flash("Giriş Başarılı!", "success")
    return response

@userBp.route("/member")
@jwt_required()
def member():
    username = session.get("userName")
    return render_template("member.html", username=username)

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

@userBp.route("/cezalarim")
@jwt_required()
def cezalarim():
    return render_template("cezalarim.html")

@userBp.route("/memberInfo")
@jwt_required()
def memberInfo():
    memberID = get_jwt_identity()
    member = None
    if memberID:
        memberObj = UserRepository.getUserById(memberID)
        if memberObj:
            member = {"username": memberObj.username, "email": memberObj.email}
    return render_template("memberInfo.html", member=member)


@userBp.route("/islemGecmisi")
@jwt_required()
def islemGecmisi():
    return render_template("userLog.html")


@userBp.route("/userLogs")
@jwt_required()
def getUserLogs():
    from datetime import datetime, date
    
    memberID = get_jwt_identity()
    rows = UserLogRepository.getAll(memberID)
    
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


@userBp.route('/kullaniciProfilGuncelle', methods=['POST'])
@jwt_required()
def kullaniciProfilGuncelle():
    data = request.get_json()
    memberID = get_jwt_identity()
    if not memberID:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    username = data.get('username')
    email = data.get('email')
    UserRepository.updateMember(memberID, username, email)
    UserLogRepository.updateUsername(memberID, username)
    session['userName'] = username
    return jsonify({"success": True, "message": "Profil güncellendi"})


@userBp.route('/kullaniciSifreDegistir', methods=['POST'])
@jwt_required()
def kullaniciSifreDegistir():
    data = request.get_json()
    memberID = get_jwt_identity()
    if not memberID:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    new_password_confirm = data.get('new_password_confirm')
    if new_password != new_password_confirm:
        return jsonify({"success": False, "message": "Yeni şifreler eşleşmiyor"}), 400

    ok, msg = UserRepository.changePassword(memberID, old_password, new_password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400

    return jsonify({"success": True, "message": msg})


@userBp.route('/kullaniciSil', methods=['POST'])
@jwt_required()
def kullaniciSil():
    data = request.get_json()
    memberID = get_jwt_identity()
    if not memberID:
        return jsonify({"success": False, "message": "Yetkisiz"}), 401

    password = data.get('password')
    ok, msg = UserService.deleteUser(memberID, password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400

    response = jsonify({"success": True, "message": msg})
    unset_jwt_cookies(response)
    session.pop('userID', None)
    session.pop('userName', None)
    return response


@userBp.route("/logout")
def logout():
    response = redirect(url_for("user.index"))
    unset_jwt_cookies(response)
    
    session.pop("userId", None)
    session.pop("userName", None)

    flash("Çıkış yaptınız.", "info")
    return response