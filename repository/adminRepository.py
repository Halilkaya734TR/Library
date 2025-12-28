from config.db import getConnection
from models.adminModel import Admin
from repository.adminLogRepository import AdminLogRepository
from datetime import datetime
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

        AdminLogRepository.save(adminId, name, 19, datetime.now())
        AdminLogRepository.updateAdminName(adminId, name)
        return True

    @staticmethod
    def changePassword(adminId, newPassword):
        hashed = generate_password_hash(newPassword)
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE admin SET password=%s WHERE adminID=%s", (hashed, adminId))
        con.commit()
        cur.close()
        con.close()
        
        admin = AdminRepository.getAdminById(adminId)
        AdminLogRepository.save(adminId, admin.name, 20, datetime.now())
        return True, "Şifre güncellendi"

    @staticmethod
    def deleteAdmin(adminId):
        admin = AdminRepository.getAdminById(adminId)
        con = getConnection()
        cur = con.cursor()
        cur.execute("DELETE FROM admin WHERE adminID=%s", (adminId,))
        con.commit()
        cur.close()
        con.close()

        AdminLogRepository.saveParams(adminId, admin.name, 21, datetime.now(), {"adminName":admin.name})
        return True, "Hesap silindi"

    @staticmethod
    def getAllAdmins():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT adminID, adminName, email FROM admin")
        rows = cur.fetchall()
        cur.close()
        con.close()

        admins = []
        for row in rows:
            admins.append({
                "id": row["adminID"],
                "name": row["adminName"],
                "email": row["email"]
            })
        return admins

    @staticmethod
    def insertAdmin(name, email, password_hash):
        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO admin (adminName, email, password) VALUES (%s, %s, %s)",
                    (name, email, password_hash))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def deleteAdminById(adminId):
        con = getConnection()
        cur = con.cursor()
        cur.execute("DELETE FROM admin WHERE adminID=%s", (adminId,))
        con.commit()
        cur.close()
        con.close()
        return True
