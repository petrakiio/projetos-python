from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from models.dbModel import DatabaseService
import os



class Pasta:
    def __init__(self):
        self.ph = PasswordHasher()
        self.db = DatabaseService()

    def criptografar(self):
        return self.ph.hash(self.password)

    def verificar(password, hash):
        ph = PasswordHasher()
        return ph.verify(hash, password)

    def criptografarPasta(self,path):
        id_path = self.db.getId(path)

        key = Fernet.generate_key()
        fernet = Fernet(key)

        # Save in database
        self.db.saveKey(id_path, key)

        for root, dirs, files in os.walk(path):

            for file in files:

                file_path = os.path.join(root, file)

                with open(file_path, "rb") as f:
                    data = f.read()

                encrypted = fernet.encrypt(data)

                with open(file_path, "wb") as f:
                    f.write(encrypted)

    def descriptografarPasta(self,path):
        id_path = self.db.getId(path)

        key = self.db.getKey(id_path)
        fernet = Fernet(key)

        for root, dirs, files in os.walk(self.path):

            for file in files:

                file_path = os.path.join(root, file)

                with open(file_path, "rb") as f:
                    data = f.read()

                decrypted = fernet.decrypt(data)

                with open(file_path, "wb") as f:
                    f.write(decrypted)