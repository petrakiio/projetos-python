from models.dbModel import DatabaseService
from models.pastaModel import Pasta

class PastService:
    def __init__(self):
        self.db = DatabaseService()
        self.past = Pasta()
    
    def queryLocked(self,value):
        return self.db.QueryPath(value)

    def cadastrarPath(self,path,password):
        hash = self.past.criptografar(password)
        insert = self.db.InsertPath(path,hash)

        if insert:
            return self.past.criptografarPasta(path)
        else:
            return None

    def AcessPast(self,path,senha):
        hash = self.db.getHash(path)
        IsMath = self.past.verificar(senha,hash)

        if IsMath:
            self.past.descriptografarPasta(path)
            return True
        else:
            return None
        