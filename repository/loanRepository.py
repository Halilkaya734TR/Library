from datetime import date, timedelta, datetime
from config.db import getConnection
from.userLogRepository import UserLogRepository
from.userRepository import UserRepository
from.bookRepository import BookRepository

class LoanRepository:
    
    @staticmethod
    def countActiveLoans(memberID):
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) AS total FROM loan WHERE memberID = %s", (memberID,))
        
        row = cur.fetchone()
        cur.close()
        con.close()
        return row["total"]
    
    @staticmethod
    def insertLoan(memberID, bookID):
        con = getConnection()
        cur = con.cursor(dictionary = True)
        cur.execute("INSERT INTO loan (memberID, bookID, loanDate, returnDate) VALUES (%s, %s, %s, %s)",(memberID, bookID, date.today(), (date.today() + timedelta(days=15))))
        con.commit()
        cur.close()
        con.close()

        member = UserRepository.getUserById(memberID)
        bookName = BookRepository.getBookNameByID(bookID)
        UserLogRepository.saveParams(memberID, member.username, 2, datetime.now(), {"bookName":bookName})
        return True
    
    @staticmethod
    def deleteLoans(memberID, loanIDs):
        if not loanIDs:
            return False
        
        con = getConnection()
        cur = con.cursor(dictionary=True)

        format_strings = ','.join(['%s'] * len(loanIDs))
        select_query = f"""
            SELECT bookID
            FROM loan
            WHERE memberID = %s AND loanID IN ({format_strings})
        """
        params = [memberID] + loanIDs
        cur.execute(select_query, params)
        rows = cur.fetchall()

        bookNames = []
        for row in rows:
            bookName = BookRepository.getBookNameByID(row["bookID"])
            if bookName:
                bookNames.append(bookName)

        delete_query = f"""
            DELETE FROM loan
            WHERE memberID = %s AND loanID IN ({format_strings})
        """
        cur.execute(delete_query, params)
        con.commit()

        cur.close()
        con.close()

        member = UserRepository.getUserById(memberID)
        if bookNames:
            UserLogRepository.saveParams(memberID, member.username, 3, datetime.now(), {"bookName": ", ".join(bookNames)})

        return True
    
    @staticmethod
    def getBorrowedBooks(memberID):
        con = getConnection()
        cur = con.cursor(dictionary=True)

        cur.execute("SELECT loanID, bookID, loanDate, returnDate FROM loan WHERE memberID = %s", (memberID,))
        result = cur.fetchall()
        cur.close()
        con.close()
        return result
    
    @staticmethod
    def getLoansByIDs(memberID, loanIDs):
        if not loanIDs:
            return []
        
        con = getConnection()
        cur = con.cursor(dictionary=True)

        format_strings = ",".join(["%s"] * len(loanIDs))
        query = f"SELECT * FROM loan WHERE memberID = %s AND loanID IN ({format_strings})"
        params = [memberID] + loanIDs

        cur.execute(query, params)
        result = cur.fetchall()

        cur.close()
        con.close()
        return result
