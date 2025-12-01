from repository.bookRepository import BookRepository

class BookService:

    @staticmethod
    def getBooks():
        return BookRepository.getBooks()