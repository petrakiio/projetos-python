from models.dbModel import DatabaseService

class PastService:

    def query(self):
        return DatabaseService.QueryPath()