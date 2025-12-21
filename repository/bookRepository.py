from config.db import getConnection
from models.bookModel import Book

class BookRepository:

    @staticmethod
    def getBooks():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        bookMYSQLcommand = """
         SELECT 
            b.bookID AS bookID,
            b.bookName AS bookName,
            a.authorName AS authorName,
            p.publisherName AS publisherName,
            c.categoryName AS categoryName,
            b.stock AS stock
        FROM books b
        JOIN author a ON b.authorID = a.authorID
        JOIN publisher p ON b.publisherID = p.publisherID
        JOIN category c ON b.categoryID = c.categoryID;     
        """
        
        cur.execute(bookMYSQLcommand)
        rows = cur.fetchall()
        cur.close()
        con.close()

        books = []
        for row in rows:
            books.append(Book(bookID=row["bookID"], bookName=row["bookName"], authorName=row["authorName"], publisherName=row["publisherName"], categoryName=row["categoryName"], stock=row["stock"]))
        return books
    
    @staticmethod
    def isBookBorrowed(bookID):
        con = getConnection()
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM loan WHERE bookID=%s",(bookID,))
        
        count = cur.fetchone()[0]
        cur.close()
        con.close()
        return count > 0

    @staticmethod
    def insertBook(bookName, authorID, publisherID, categoryID, stock):
        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO books (bookName, authorID, publisherID, categoryID, stock) VALUES (%s,%s,%s,%s,%s)",(bookName, authorID, publisherID, categoryID, stock))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def updateBook(bookID, bookName, authorID, publisherID, categoryID, stock):
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE books SET bookName=%s, authorID=%s, publisherID=%s, categoryID=%s, stock=%s WHERE bookID=%s",(bookName, authorID, publisherID, categoryID, stock, bookID))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def deleteBooks(bookIDs):
        con = getConnection()
        cur = con.cursor()
        f = ",".join(["%s"] * len(bookIDs))
        cur.execute(f"DELETE FROM books WHERE bookID IN ({f})", bookIDs)
        
        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def decreaseStock(bookID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("UPDATE books SET stock = stock - 1 WHERE bookID = %s",(bookID,))

        con.commit()
        cur.close()
        con.close()
        return True
    
    @staticmethod
    def increaseStock(bookID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("UPDATE books SET stock = stock + 1 WHERE bookID = %s", (bookID,))
        
        con.commit()
        cur.close()
        con.close()

    @staticmethod
    def getBookNameByID(bookID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT bookName FROM books WHERE bookID=%s", (bookID,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            return row["bookName"]
        return None
