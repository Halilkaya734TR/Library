import mysql.connector

def getConnection():
    return mysql.connector.connect(host="localhost",user="root",password="710088",database="library")