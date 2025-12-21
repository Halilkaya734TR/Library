from config.db import getConnection
from models.adminModel import Admin
from werkzeug.security import generate_password_hash, check_password_hash

class AdminRepository:

    @staticmethod
    def getAdminByMail(mail):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM admin WHERE email=%s", (mail,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return Admin(id=row["adminID"], name=row["adminName"], mail = row["email"], sifre= row["password"])
        
        return None

    @staticmethod
    def getAdminById(adminId):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM admin WHERE adminID=%s", (adminId,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return Admin(id=row["adminID"], name=row["adminName"], mail=row["email"], sifre=row["password"])
        return None

    @staticmethod
    def updateAdmin(adminId, name, mail):
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE admin SET adminName=%s, email=%s WHERE adminID=%s", (name, mail, adminId))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def changePassword(adminId, old_password, new_password):
        admin = AdminRepository.getAdminById(adminId)
        if not admin:
            return False, "Admin bulunamadı"

        if not check_password_hash(admin.sifre, old_password):
            return False, "Eski şifre yanlış"

        hashed = generate_password_hash(new_password)
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE admin SET password=%s WHERE adminID=%s", (hashed, adminId))
        con.commit()
        cur.close()
        con.close()
        return True, "Şifre güncellendi"

    @staticmethod
    def deleteAdmin(adminId, password):
        admin = AdminRepository.getAdminById(adminId)
        if not admin:
            return False, "Admin bulunamadı"

        if not check_password_hash(admin.sifre, password):
            return False, "Şifre yanlış"

        con = getConnection()
        cur = con.cursor()
        cur.execute("DELETE FROM admin WHERE adminID=%s", (adminId,))
        con.commit()
        cur.close()
        con.close()
        return True, "Hesap silindi"