from config.db import getConnection
from models.authorModel import Author

class AuthorRepository:

    @staticmethod
    def getAuthors():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT authorID, authorName FROM author")
        
        rows = cur.fetchall()
        cur.close()
        con.close()

        author = []
        for row in rows:
            author.append(Author(authorID=row["authorID"], authorName=row["authorName"]))
        return author

    @staticmethod
    def insertAuthor(authorName):
        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO author (authorName) VALUES (%s)", (authorName,))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def updateAuthor(authorID, authorName):
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE author SET authorName=%s WHERE authorID=%s", (authorName, authorID))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def deleteAuthors(authorIDs):
        con = getConnection()
        cur = con.cursor()
        for aid in authorIDs:
            cur.execute("SELECT COUNT(*) FROM books WHERE authorID=%s", (aid,))
            cnt = cur.fetchone()[0]
            if cnt > 0:
                cur.close()
                con.close()
                raise Exception(f"linked:{aid}")

        f = ",".join(["%s"] * len(authorIDs))
        cur.execute(f"DELETE FROM author WHERE authorID IN ({f})", authorIDs)
        con.commit()
        cur.close()
        con.close()
        return True
