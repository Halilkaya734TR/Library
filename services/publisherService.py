from repository.publisherRepository import PublisherRepository

class PublisherService:

    @staticmethod
    def getPublishers():
        return PublisherRepository.getPublishers()

    @staticmethod
    def addPublisher(data):
        return PublisherRepository.insertPublisher(data.get("publisherName"))

    @staticmethod
    def editPublisher(data):
        return PublisherRepository.updatePublisher(data.get("publisherID"), data.get("publisherName"))

    @staticmethod
    def deletePublisher(ids):
        return PublisherRepository.deletePublisher(ids)
