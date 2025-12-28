from repository.loanRepository import LoanRepository
from services.bookService import BookService
from datetime import datetime, date

class BorrowService:
    
    @staticmethod
    def getActiveLoan(memberID):
        return LoanRepository.countActiveLoans(memberID)
    
    @staticmethod
    def borrowBook(memberID, bookID):
        return LoanRepository.insertLoan(memberID, bookID)
  
    @staticmethod
    def getBorrowedBookDetailed(memberID):
        loans = LoanRepository.getBorrowedBooks(memberID)

        if not loans:
            return []

        books = BookService.getBooks()    
        result = []

        for loan in loans:
            book = next((b for b in books if b.bookID == loan["bookID"]), None)
            if not book:
                continue

            ld = loan["loanDate"]
            rd = loan["returnDate"]

            def fmt(d):
                if isinstance(d, datetime):
                    return d.strftime("%d.%m.%Y %H:%M")
                if isinstance(d, date):
                    return d.strftime("%d.%m.%Y")
                return str(d) if d is not None else ""

            result.append({
                "loanID": loan["loanID"],
                "bookID": loan["bookID"],
                "bookName": book.bookName,
                "author": book.authorName,
                "loanDate": fmt(ld),
                "returnDate": fmt(rd)
            })

        return result

    @staticmethod
    def returnBooks(memberID, loanIDs):
        int_ids = [int(x) for x in loanIDs]

        loans = LoanRepository.getLoansByIDs(memberID, int_ids)

        for loan in loans:
            BookService.increaseStock(loan["bookID"])

        LoanRepository.deleteLoans(memberID, int_ids)
        return True

    