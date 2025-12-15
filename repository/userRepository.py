from datetime import date
from config.db import getConnection
from models.userModel import User

class UserRepository:

    @staticmethod
    def getUserByMail(email):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM member WHERE email=%s", (email,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return User(memberID=row["memberID"], username=row["username"], email=row["email"], password=row["password"], joinDate=row["joinDate"], status=row["status"])
        
        return None
    
    @staticmethod
    def createUser(username, email, password):
        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO member (username, email, password, joinDate, status) VALUES (%s, %s, %s, %s, %s)",(username, email, password, date.today(), 'Aktif'))
        con.commit()
        cur.close()
        con.close()

        return True