from config.db import getConnection
from models.categoryModel import Category

class CategoryRepository:

    @staticmethod
    def getCategories():
        con = getConnection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT categoryID, categoryName FROM category")
        
        rows = cur.fetchall()
        cur.close()
        con.close()

        category = []
        for row in rows:
            category.append(Category(categoryID=row["categoryID"], categoryName=row["categoryName"]))
        return category
    
    @staticmethod
    def insertCategory(categoryName):
        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO category (categoryName) VALUES (%s)", (categoryName,))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def updateCategory(categoryID, categoryName):
        con = getConnection()
        cur = con.cursor()
        cur.execute("UPDATE category SET categoryName=%s WHERE categoryID=%s", (categoryName, categoryID))
        con.commit()
        cur.close()
        con.close()
        return True

    @staticmethod
    def deleteCategories(categoryIDs):
        con = getConnection()
        cur = con.cursor()
        
        for cid in categoryIDs:
            cur.execute("SELECT COUNT(*) FROM books WHERE categoryID=%s", (cid,))
            cnt = cur.fetchone()[0]
            if cnt > 0:
                cur.close()
                con.close()
                raise Exception(f"linked:{cid}")

        f = ",".join(["%s"] * len(categoryIDs))
        cur.execute(f"DELETE FROM category WHERE categoryID IN ({f})", categoryIDs)
        con.commit()
        cur.close()
        con.close()
        return True