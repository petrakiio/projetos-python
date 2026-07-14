import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class DatabaseService:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        
    def getConnection(self):
        try:
            connection = mysql.connector(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database
            )
            return connection
        except Exception as err:
            print(f'Error:{err}')
            return None
    
    def InsertPath(self,pathModel):
        pathModel.criptografar()
        db = None

        try:
            db = self.getConnection()
            cursor = db.cursor()
            sql = 'INSERT INTO Path(path,password) VALUES (%s,%s)'

            values = (pathModel.path,pathModel.password)
            cursor.execute(sql,values)

            db.commit()
            db.close()
            cursor.close()

            return True
        except Exception as err:
            print(f'Error:{err}')
            return None
