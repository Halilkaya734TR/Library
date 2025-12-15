from datetime import date, timedelta
from config.db import getConnection

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
        return True
    
    @staticmethod
    def deleteLoans(memberID, loanIDs):
        if not loanIDs:
            return False
        
        con = getConnection()
        cur = con.cursor(dictionary=True)
        format_strings = ','.join(['%s'] * len(loanIDs))
        query = f"DELETE FROM loan WHERE memberID = %s AND loanID IN ({format_strings})"
        params = [memberID] + loanIDs

        cur.execute(query, params)
        con.commit()
        cur.close()
        con.close()
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
