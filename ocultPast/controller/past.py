from models.db import DatabaseService

class PastService:

    def query(self):
        return DatabaseService.QueryPath()