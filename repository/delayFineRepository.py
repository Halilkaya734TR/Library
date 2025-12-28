from config.db import getConnection
from models.delayFineModel import delayFine
from repository.userRepository import UserRepository
from repository.userLogRepository import UserLogRepository
from datetime import datetime

class DelayFineRepository:

    @staticmethod
    def countactiveFine(userID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) AS total FROM delayFine WHERE userID = %s", (userID,))
        
        row = cur.fetchone()
        cur.close()
        con.close()
        return row["total"]
    
    @staticmethod
    def getByUserID(userID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        mySQLCommand ="""
            SELECT ID, userID, bookID, delay, sum, firstDay 
            FROM delayFine 
            WHERE userID = %s 
            ORDER BY firstDay DESC
        """
        cur.execute(mySQLCommand, (userID,))
        
        rows = cur.fetchall()
        cur.close()
        con.close()
        
        fines = []
        for row in rows:
            fines.append(delayFine(
                ID=row["ID"],
                userID=row["userID"],
                bookID=row["bookID"],
                delay=row["delay"],
                sum=row["sum"],
                firstDay=row["firstDay"]
            ))
        return fines

    @staticmethod
    def getAll():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        mySQLCommand = """
            SELECT 
                d.ID, 
                d.userID, 
                d.bookID, 
                d.delay, 
                d.sum, 
                d.firstDay,
                m.username AS userName,
                b.bookName AS bookName
            FROM delayFine d
            LEFT JOIN member m ON m.memberID = d.userID
            LEFT JOIN books b ON b.bookID = d.bookID
            ORDER BY d.firstDay DESC
        """
        cur.execute(mySQLCommand)
        
        rows = cur.fetchall()
        cur.close()
        con.close()
        
        return rows
    
    @staticmethod
    def getFinesForMailByIDs(cezaIDs):
        if not cezaIDs:
            return []

        con = getConnection()
        cur = con.cursor(dictionary=True)
        placeholders = ",".join(["%s"] * len(cezaIDs))
        
        query = f"""
            SELECT
                d.ID AS fineID,
                d.sum,
                d.firstDay,
                b.bookName,
                m.memberID,
                m.username,
                m.email
            FROM delayFine d
            JOIN books b ON b.bookID = d.bookID
            JOIN member m ON m.memberID = d.userID
            WHERE d.ID IN ({placeholders})
        """

        cur.execute(query, cezaIDs)
        rows = cur.fetchall()

        cur.close()
        con.close()
        return rows


    @staticmethod
    def deleteByUserID(userID):
        con = getConnection()
        cur = con.cursor()
        cur.execute("DELETE FROM delayFine WHERE userID = %s", (userID,))
        
        con.commit()
        cur.close()
        con.close()

        member = UserRepository.getUserById(userID)
        UserLogRepository.save(userID, member.username, 24, datetime.now())
        return True
