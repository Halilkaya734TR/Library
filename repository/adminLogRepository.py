import json
from config.db import getConnection

class AdminLogRepository:

    @staticmethod
    def save(adminID, adminName, logID, logDate):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("INSERT INTO adminLog (adminID, adminName, logID, logDate) VALUES (%s, %s, %s, %s)", (adminID, adminName, logID, logDate))

        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def saveParams(adminID, adminName, logID, logDate, logParams):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("INSERT INTO adminLog (adminID, adminName, logID, logDate, logParams) VALUES (%s, %s, %s, %s, %s)", (adminID, adminName, logID, logDate, json.dumps(logParams)))

        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def updateAdminName(adminID, adminName):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        sql = "UPDATE adminLog SET adminName = %s WHERE adminID = %s"
        cur.execute(sql, (adminName, adminID))
        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def getAllLogs():
        con = getConnection()
        cur = con.cursor(dictionary=True)

        cur.execute("""
            SELECT
                al.adminID,
                al.adminName,
                al.logDate,
                lm.messageTemplate,
                al.logParams
            FROM adminLog al
            LEFT JOIN logMessages lm ON al.logID = lm.logID
            ORDER BY al.logDate DESC
        """)

        rows = cur.fetchall()
        cur.close()
        con.close()

        for row in rows:
            message = row["messageTemplate"] or "İşlem"

            if row["logParams"]:
                try:
                    params = row["logParams"]
                    if isinstance(params, str):
                        params = json.loads(params)
                    if isinstance(params, dict):
                        for key, value in params.items():
                            message = message.replace(f"{{{key}}}", str(value))
                except:
                    pass

            row["logMessage"] = message
        return rows
