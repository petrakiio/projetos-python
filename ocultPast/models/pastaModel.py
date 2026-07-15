from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from models.dbModel import DatabaseService
import os

fernet = Fernet(key)

with open("teste.txt", "rb") as f:
    dados = f.read()

dados_criptografados = fernet.encrypt(dados)

with open("teste.txt", "wb") as f:
    f.write(dados_criptografados)


class Pasta:
    def __init__(self, path, password):
        self.path = path
        self.password = password
        self.ph = PasswordHasher()
        self.db = DatabaseService()

    def criptografar(self):
        return self.ph.hash(self.password)

    @staticmethod
    def verificar(password, hash):
        ph = PasswordHasher()
        return ph.verify(hash, password)

    def criptografarPasta(self,path):
        