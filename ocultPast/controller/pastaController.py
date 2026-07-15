from models.dbModel import DatabaseService

class PastService:
    def __init__(self):
        self.db = DatabaseService()

    def query(self):
        return self.db.QueryPath()