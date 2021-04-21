from core.database.db_connect import Connection
from pypika import Query, Table

superban = Table("superban_table")

class SuperbanRepository(Connection):
    def getById(self, args=None):
        query = Query.from_(superban).select("*").where(superban.user_id == '%s')
        q = query.get_sql(quote_char=None)

        return self._select(q, args)

    def getAll(self, args=None):
        q = "SELECT * FROM superban_table LIMIT %s,%s"

        return self._selectAll(q, args)

    def getLastSuperBanned(self):
        q = "SELECT * FROM superban_table WHERE user_date BETWEEN DATE_SUB(NOW(), INTERVAL 15 DAY) AND NOW() ORDER BY user_date DESC LIMIT 10"

        return self._selectAll(q)

    def getCountSuperBanned(self):
        q = 'SELECT COUNT(*) AS counter FROM superban_table'

        return self._select(q)

    def add(self, args=None):
        q = "INSERT IGNORE INTO superban_table(user_id, motivation_text, user_date, id_operator) VALUES (%s,%s,%s,%s)"
        return self._insert(q, args)