from config.db import getConnection
from models.adminModel import Admin

class AdminRepository:

    @staticmethod
    def getAdminByMail(mail):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM adminler WHERE adminMail=%s", (mail,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return Admin(id=row["adminId"], name=row["adminAd"], mail = row["adminMail"], sifre= row["adminSifre"])
        
        return None