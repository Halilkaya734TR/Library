from config.db import getConnection
from models.publisherModel import Publisher

class PublisherRepository:

    @staticmethod
    def getPublishers():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT publisherID, publisherName FROM publisher")
        
        rows = cur.fetchall()
        cur.close()
        con.close()

        publishers = []
        for row in rows:
            publishers.append(Publisher(publisherID=row["publisherID"], publisherName=row["publisherName"]))
        return publishers

    @staticmethod
    def insertPublisher(publisherName):
        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO publisher (publisherName) VALUES (%s)", (publisherName,))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def updatePublisher(publisherID, publisherName):
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE publisher SET publisherName=%s WHERE publisherID=%s", (publisherName, publisherID))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def deletePublisher(publisherIDs):
        con = getConnection()
        cur = con.cursor()
        
        for cid in publisherIDs:
            cur.execute("SELECT COUNT(*) FROM books WHERE publisherID=%s", (cid,))
            cnt = cur.fetchone()[0]
            if cnt > 0:
                cur.close()
                con.close()
                raise Exception(f"linked:{cid}")

        f = ",".join(["%s"] * len(publisherIDs))
        cur.execute(f"DELETE FROM publisher WHERE publisherID IN ({f})", publisherIDs)
        con.commit()
        cur.close()
        con.close()
        return True