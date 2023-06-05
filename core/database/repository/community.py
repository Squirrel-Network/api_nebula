#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core.database.db_connect import Connection
from pypika import Query, Table

community = Table("community")


class CommunityRepository(Connection):
    def getById(self, args=None):
        query = Query.from_(community).select("*").where(community.tg_group_id == "%s")
        q = query.get_sql(quote_char=None)

        return self._select(q, args)

    def getAll(self):
        query = Query.from_(community).select("*")
        q = query.get_sql(quote_char=None)

        return self._selectAll(q)

    def top_ten_communities(self, args=None):
        q = "SELECT nu.tg_group_id,gr.group_name,co.tg_group_link,gr.group_photo,co.language,co.type,gr.total_users,COUNT(nu.update_id) AS counter FROM nebula_updates nu INNER JOIN groups gr ON gr.id_group = nu.tg_group_id INNER JOIN community co ON co.tg_group_id = gr.id_group WHERE nu.tg_group_id NOT IN (-1001267698171)AND gr.community = 1 GROUP BY nu.tg_group_id ORDER BY counter DESC LIMIT 50"

        return self._selectAll(q)
