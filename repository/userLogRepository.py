import json
from config.db import getConnection
class UserLogRepository:

    @staticmethod
    def save(userID, username, logID, logDate):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("INSERT INTO userLog (userID, username, logID, logDate) VALUES (%s, %s, %s, %s)", (userID, username, logID, logDate))

        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def saveParams(userID, username, logID, logDate, logParams):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("INSERT INTO userLog (userID, username, logID, logDate, logParams) VALUES (%s, %s, %s, %s, %s)", (userID, username, logID, logDate,json.dumps(logParams)))

        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def updateUsername(userID, username):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        sql = "UPDATE userLog SET username = %s WHERE userID = %s"
        cur.execute(sql, (username, userID))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def getAll(userID):
        con = getConnection()
        cur = con.cursor(dictionary=True)

        cur.execute("""
            SELECT
                ul.userID,
                ul.username,
                ul.logDate,
                lm.messageTemplate,
                ul.logParams
            FROM userLog ul
            LEFT JOIN logMessages lm ON ul.logID = lm.logID
            WHERE ul.userID = %s
            ORDER BY ul.logDate DESC
        """, (userID,))

        rows = cur.fetchall()
        cur.close()
        con.close()

        for row in rows:
            message = row["messageTemplate"]

            if row["logParams"]:
                params = json.loads(row["logParams"])
                for key, value in params.items():
                    message = message.replace(f"{{{key}}}", str(value))

            row["logMessage"] = message
        return rows