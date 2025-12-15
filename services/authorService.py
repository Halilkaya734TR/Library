from repository.authorRepository import AuthorRepository

class AuthorService:

    @staticmethod
    def getAuthors():
        return AuthorRepository.getAuthors()

    @staticmethod
    def addAuthor(data):
        return AuthorRepository.insertAuthor(data.get("authorName"))

    @staticmethod
    def editAuthor(data):
        return AuthorRepository.updateAuthor(data.get("authorID"), data.get("authorName"))

    @staticmethod
    def deleteAuthors(ids):
        return AuthorRepository.deleteAuthors(ids)