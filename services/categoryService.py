from repository.categoryRepository import CategoryRepository

class CategoryService:

    @staticmethod
    def getCategories():
        return CategoryRepository.getCategories()

    @staticmethod
    def addCategory(data):
        return CategoryRepository.insertCategory(data.get("categoryName"))

    @staticmethod
    def editCategory(data):
        return CategoryRepository.updateCategory(data.get("categoryID"), data.get("categoryName"))

    @staticmethod
    def deleteCategories(ids):
        return CategoryRepository.deleteCategories(ids)
