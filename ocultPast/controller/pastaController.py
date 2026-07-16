from models.dbModel import DatabaseService
from models.pastaModel import Pasta

class PastService:
    def __init__(self):
        self.db = DatabaseService()
        self.past = Pasta()

    def queryOnlocked(self):
        return self.db.QueryPath()
    
    def queryLocked(self):
        

    def AcessPast(self,path,senha):
        hash = self.db.getHash(path)
        IsMath = self.past.verificar(senha,hash)

        if IsMath:
            self.past.descriptografarPasta(path)
            return True
        else:
            return None