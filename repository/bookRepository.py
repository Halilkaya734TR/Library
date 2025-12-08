from config.db import getConnection
from models.bookModel import Book

class BookRepository:

    @staticmethod
    def getBooks():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT bookId AS id, bookName AS name, author, publisher, category, pageNumber FROM kitaplar")
        rows = cur.fetchall()
        cur.close()
        con.close()

        books = []
        for row in rows:
            books.append(Book(id=row["id"], name=row["name"], author=row["author"], publisher=row["publisher"], category=row["category"], pageNumber=row["pageNumber"]))
        return books