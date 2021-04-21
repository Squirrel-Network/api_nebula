from core.database.db_connect import Connection
from pypika import Query, Table

users = Table("users")

class UserRepository(Connection):
    def getById(self, args=None):
        query = Query.from_(users).select("*").where(users.tg_id == "%s")
        q = query.get_sql(quote_char=None)

        return self._select(q, args)

    def getByUsername(self, args=None):
        q = "SELECT * FROM users WHERE tg_username = %s"

        return self._select(q, args)

    def getAllbyId(self, args=None):
        query = Query.from_(users).select("*").where(users.tg_id == "%s")
        q = query.get_sql(quote_char=None)

        return self._selectAll(q, args)

    def getAll(self,args=None):
        print(args)
        q = "SELECT * FROM users LIMIT %s,%s"
        print(q)
        #query = Query.from_(users).select("*")
        #q = query.get_sql(quote_char=None)
        return self._selectAll(q,args)

    def add(self, args=None):
        q = "INSERT INTO users (tg_id, tg_username, warn_count) VALUES (%s,%s,%s)"
        return self._insert(q, args)

    def update(self, args=None):
        q = "UPDATE users SET tg_username = %s WHERE tg_id = %s"
        return self._update(q,args)

    def getCountUsers(self):
        q = 'SELECT COUNT(*) AS counter FROM users'

        return self._select(q)

    def deleteUser(self, args=None):
        q = "DELETE FROM users WHERE tg_id = %s"
        print(args)
        return self._delete(q,args)