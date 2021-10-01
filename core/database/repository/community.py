#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core.database.db_connect import Connection
from pypika import Query, Table

community = Table("community")


class CommunityRepository(Connection):
    def getById(self, args=None):
        query = Query.from_(community).select("*").where(community.tg_group_id == '%s')
        q = query.get_sql(quote_char=None)

        return self._select(q, args)

    def getAll(self):
        query = Query.from_(community).select("*")
        q = query.get_sql(quote_char=None)

        return self._selectAll(q)