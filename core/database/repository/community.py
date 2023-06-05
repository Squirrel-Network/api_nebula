#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class CommunityRepository(Connection):
    def get_by_id(self, tg_group_id: int):
        q = "SELECT * FROM community WHERE tg_group_id = %s"

        return self._select(q, (tg_group_id,))

    def get_all(self):
        q = "SELECT * FROM community"

        return self._select_all(q)

    def top_ten_communities(self):
        q = "SELECT nu.tg_group_id,gr.group_name,co.tg_group_link,gr.group_photo,co.language,co.type,gr.total_users,COUNT(nu.update_id) AS counter FROM nebula_updates nu INNER JOIN groups gr ON gr.id_group = nu.tg_group_id INNER JOIN community co ON co.tg_group_id = gr.id_group WHERE nu.tg_group_id NOT IN (-1001267698171)AND gr.community = 1 GROUP BY nu.tg_group_id ORDER BY counter DESC LIMIT 50"

        return self._select_all(q)
