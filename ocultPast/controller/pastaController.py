from models.dbModel import DatabaseService
from models.pastaModel import Pasta

class PastService:
    def __init__(self):
        self.db = DatabaseService()
        self.past = Pasta()

    def query(self):
        return self.db.QueryPath()

    def Validate(self,path,senha):
        hash = self.db.OneQuery(path)
        IsMath = self.past.verificar(senha,hash)