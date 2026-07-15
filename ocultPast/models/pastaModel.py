from argon2 import PasswordHasher


class Pasta:
    def __init__(self, path, password):
        self.path = path
        self.password = password
        self.ph = PasswordHasher()

    def criptografar(self):
        return self.ph.hash(self.password)

    @staticmethod
    def verificar(password, hash):
        ph = PasswordHasher()
        return ph.verify(hash, password)
