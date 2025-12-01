from config.db import getConnection
from models.userModel import User

class UserRepository:

    @staticmethod
    def getUserByMail(mail):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM kullanicilar WHERE mail=%s", (mail,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return User(id=row["kullaniciId"], name=row["kullaniciAdi"], mail = row["mail"], sifre= row["sifre"])
        
        return None