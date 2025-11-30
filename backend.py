from flask import Flask, request, redirect, render_template, session, flash, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key = "HeasPoty!l01Zs"

con = mysql.connector.connect(host="localhost",user="root",password="710088",database="library")

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/userLogin", methods=["POST"])
def user_login():
    mail = request.form.get("mail")
    sifre = request.form.get("sifre")
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM kullanicilar WHERE mail=%s",(mail,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user["sifre"], sifre):
        session["userId"] = user["kullaniciId"]
        session["userName"] = user["kullaniciAdi"]
        flash("Giriş başarılı!", "success")
        return redirect(url_for("member"))
    else:
        flash("Girilen bilgiler uyuşmuyor!", "danger")
        return redirect(url_for("index"))

@app.route("/member", methods=["GET"])
def member():
    if "userId" in session:
        return render_template("member.html")
    else:
        flash("Önce giriş yapmalısınız!", "danger")
        return redirect(url_for("index"))
    
if __name__ == "__main__":
    app.run(debug=True)