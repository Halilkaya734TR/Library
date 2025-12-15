from repository.bookRepository import BookRepository

class BookService:

    @staticmethod
    def getBooks():
        return BookRepository.getBooks()
    
    @staticmethod
    def addBook(data):
        return BookRepository.insertBook(
            data["bookName"],
            data["authorID"],
            data["publisherID"],
            data["categoryID"],
            data["stock"]
        )

    @staticmethod
    def editBook(data):
        return BookRepository.updateBook(
            data["bookID"],
            data["bookName"],
            data["authorID"],
            data["publisherID"],
            data["categoryID"],
            data["stock"]
        )

    @staticmethod
    def deleteBooks(ids):
        for bookID in ids:
            if BookRepository.isBookBorrowed(bookID):
                raise Exception("borrowed")
        return BookRepository.deleteBooks(ids)
   
    
    @staticmethod
    def decreaseStock(bookID):
        return BookRepository.decreaseStock(bookID)
    
    @staticmethod
    def increaseStock(bookID):
        return BookRepository.increaseStock(bookID)