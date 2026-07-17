from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from models.dbModel import DatabaseService
import os


class Pasta:

    def __init__(self):
        self.ph = PasswordHasher()
        self.db = DatabaseService()


    def criptografar(self, password):
        return self.ph.hash(password)


    @staticmethod
    def verificar(password, hash):
        ph = PasswordHasher()

        try:
            return ph.verify(hash, password)

        except Exception:
            return False


    def criptografarPasta(self, path):

        id_path = self.db.getId(path)

        if id_path is None:
            return False


        key = Fernet.generate_key()

        fernet = Fernet(key)


        # salva chave
        self.db.saveKey(id_path, key)


        for root, dirs, files in os.walk(path):

            for file in files:

                file_path = os.path.join(root, file)


                with open(file_path, "rb") as f:
                    data = f.read()


                encrypted = fernet.encrypt(data)


                with open(file_path, "wb") as f:
                    f.write(encrypted)


        # bloqueia pasta
        self.db.updateAcess(id_path, False)

        return True



    def descriptografarPasta(self, path):

        id_path = self.db.getId(path)

        if id_path is None:
            return False


        key = self.db.getKey(id_path)

        if key is None:
            return False


        fernet = Fernet(key)


        try:

            for root, dirs, files in os.walk(path):

                for file in files:

                    file_path = os.path.join(root, file)


                    with open(file_path, "rb") as f:
                        data = f.read()


                    decrypted = fernet.decrypt(data)


                    with open(file_path, "wb") as f:
                        f.write(decrypted)

            # debloqueia a pasta
            self.db.updateAcess(id_path, True)

            return True


        except Exception as err:

            print(f"Erro ao descriptografar: {err}")

            return False