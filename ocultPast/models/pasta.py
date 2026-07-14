from argon2 import PasswordHasher

class pasta:
    def __init__(self,path,password):
        self.path = path
        self.password = password
        self.ph = PasswordHasher()
    
    def criptografar(self):
        self.ph.hash(self.password)
    
    staticmethod
    def verific(self,password,hash):
        if self.ph.verify(hash,password):
            return True
        else:
            return False