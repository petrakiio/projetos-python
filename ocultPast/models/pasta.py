from argon2 import PasswordHasher

class pasta:
    def __init__(self,path,password):
        self.path = path
        self.password = password
        self.ph = PasswordHasher()
    
    def criptografar(self):
        self.ph.hash(self.password)
        self.ph.hash(self.path)