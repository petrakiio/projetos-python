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
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            return connection

        except Exception as err:
            print(f"Erro ao conectar ao banco: {err}")
            return None


    def InsertPath(self, pathModel):
        db = None
        cursor = None

        try:
            pathModel.password = pathModel.criptografar()

            db = self.getConnection()

            if db is None:
                return False

            cursor = db.cursor()

            sql = """
                INSERT INTO Path (path, password)
                VALUES (%s, %s)
            """

            values = (
                pathModel.path,
                pathModel.password
            )

            cursor.execute(sql, values)
            db.commit()

            return True

        except Exception as err:
            print(f"Erro: {err}")
            return False

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()


    def QueryPath(self, value):
        db = None
        cursor = None

        try:
            db = self.getConnection()

            if db is None:
                return None

            cursor = db.cursor()

            sql = """
                SELECT path 
                FROM Path 
                WHERE unlocked = %s
            """

            cursor.execute(sql, (value,))

            return cursor.fetchall()

        except Exception as err:
            print(f"Erro: {err}")
            return None

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()


    def getHash(self, path):
        db = None
        cursor = None

        try:
            db = self.getConnection()

            if db is None:
                return None

            cursor = db.cursor()

            sql = """
                SELECT password 
                FROM Path 
                WHERE path = %s
            """

            cursor.execute(sql, (path,))

            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        except Exception as err:
            print(f"Erro: {err}")
            return None

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()


    def getId(self, path):
        db = None
        cursor = None

        try:
            db = self.getConnection()

            if db is None:
                return None

            cursor = db.cursor()

            sql = """
                SELECT id 
                FROM Path 
                WHERE path = %s
            """

            cursor.execute(sql, (path,))

            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        except Exception as err:
            print(f"Erro: {err}")
            return None

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()


    def saveKey(self, path_id, key):
        db = None
        cursor = None

        try:
            db = self.getConnection()

            if db is None:
                return False

            cursor = db.cursor()

            sql = """
                INSERT INTO PathKeys(path_id, encrypted_key)
                VALUES (%s, %s)
            """

            values = (
                path_id,
                key
            )

            cursor.execute(sql, values)

            db.commit()

            return True

        except Exception as err:
            print(f"Erro: {err}")
            return False

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()


    def getKey(self, path_id):
        db = None
        cursor = None

        try:
            db = self.getConnection()

            if db is None:
                return None

            cursor = db.cursor()

            sql = """
                SELECT encrypted_key 
                FROM PathKeys 
                WHERE path_id = %s
            """

            cursor.execute(sql, (path_id,))

            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        except Exception as err:
            print(f"Erro: {err}")
            return None

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()