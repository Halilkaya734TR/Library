from config.db import getConnection
from models.bookModel import Book

class BookRepository:

    @staticmethod
    def getBooks():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT kitapId AS id, kitapAdi AS ad, yazar, yayinevi FROM kitaplar")
        rows = cur.fetchall()
        cur.close()
        con.close()

        books = []
        for row in rows:
            books.append(Book(id=row["id"], ad=row["ad"], yazar=row["yazar"], yayinevi=row["yayinevi"]))
        return books