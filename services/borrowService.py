from repository.loanRepository import LoanRepository
from services.bookService import BookService

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

            result.append({
                "loanID": loan["loanID"],
                "bookID": loan["bookID"],
                "bookName": book.bookName,
                "author": book.authorName,
                "loanDate": str(loan["loanDate"]),
                "returnDate": str(loan["returnDate"])
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

    