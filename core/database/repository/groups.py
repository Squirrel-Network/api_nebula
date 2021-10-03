#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core.database.db_connect import Connection
from pypika import Query, Table

groups = Table("groups")


class GroupRepository(Connection):
    def getById(self, args=None):
        query = Query.from_(groups).select("*").where(groups.id_group == '%s')
        q = query.get_sql(quote_char=None)

        return self._select(q, args)

    def getAll(self):
        query = Query.from_(groups).select("*")
        q = query.get_sql(quote_char=None)

        return self._selectAll(q)

    def top_ten_groups(self, args=None):
        q = 'SELECT nu.tg_group_id,gr.group_name,COUNT(nu.update_id) AS counter FROM nebula_updates nu INNER JOIN groups gr ON gr.id_group = nu.tg_group_id WHERE nu.tg_group_id NOT IN (-1001267698171) GROUP BY nu.tg_group_id ORDER BY counter DESC LIMIT 10'

        return self._selectAll(q)