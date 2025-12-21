from datetime import date, datetime
from config.db import getConnection
from models.userModel import User
from repository.userLogRepository import UserLogRepository
from werkzeug.security import generate_password_hash, check_password_hash

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
        userID = cur.lastrowid
        cur.close()
        con.close()

        UserLogRepository.saveParams(userID, username, 1, datetime.now(), {"username": username})
        return True
    
    @staticmethod
    def getUserById(memberID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM member WHERE memberID=%s", (memberID,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return User(memberID=row["memberID"], username=row["username"], email=row["email"], password=row["password"], joinDate=row["joinDate"], status=row["status"])
        return None

    @staticmethod
    def updateMember(memberID, username, email):
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE member SET username=%s, email=%s WHERE memberID=%s", (username, email, memberID))
        con.commit()
        cur.close()
        con.close()

        UserLogRepository.save(memberID, username, 4, datetime.now())
        UserLogRepository.updateUsername(memberID, username)
        return True

    @staticmethod
    def changePassword(memberID, old_password, new_password):
        member = UserRepository.getUserById(memberID)
        if not member:
            return False, "Kullanıcı bulunamadı"

        if not check_password_hash(member.password, old_password):
            return False, "Eski şifre yanlış"

        hashed = generate_password_hash(new_password)
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE member SET password=%s WHERE memberID=%s", (hashed, memberID))
        con.commit()
        cur.close()
        con.close()
        
        UserLogRepository.save(memberID, member.username, 5, datetime.now())
        return True, "Şifre güncellendi"

    @staticmethod
    def checkUnreturnedBooks(memberID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) as count FROM loan WHERE memberID=%s", (memberID,))
        row = cur.fetchone()
        cur.close()
        con.close()
        return row["count"] if row else 0

    @staticmethod
    def deleteUser(memberID, password):
        member = UserRepository.getUserById(memberID)
        if not member:
            return False, "Kullanıcı bulunamadı"

        if not check_password_hash(member.password, password):
            return False, "Şifre yanlış"

        unreturned = UserRepository.checkUnreturnedBooks(memberID)
        if unreturned > 0:
            return False, f"Hesabınızı silmeden önce {unreturned} adet iade edilmemiş kitapı iade etmelisiniz"

        con = getConnection()
        cur = con.cursor()
        cur.execute("DELETE FROM member WHERE memberID=%s", (memberID,))
        con.commit()
        cur.close()
        con.close()

        UserLogRepository.saveParams(memberID, member.username, 6, datetime.now(), {"username": member.username})
        return True, "Hesap silindi"