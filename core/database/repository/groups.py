#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class GroupRepository(Connection):
    def get_by_id(self, id_group: int):
        q = "SELECT * FROM groups WHERE id_group = %s"

        return self._select(q, (id_group,))

    def get_all(self):
        q = "SELECT * FROM groups"

        return self._select_all(q)

    def top_ten_groups(self):
        q = "SELECT nu.tg_group_id,gr.group_name,co.tg_group_link,gr.group_photo,co.language,co.type,gr.total_users,COUNT(nu.update_id) AS counter FROM nebula_updates nu INNER JOIN groups gr ON gr.id_group = nu.tg_group_id INNER JOIN community co ON co.tg_group_id = gr.id_group WHERE nu.tg_group_id NOT IN (-1001267698171)AND gr.updated_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()AND gr.community = 1 GROUP BY nu.tg_group_id ORDER BY counter DESC LIMIT 10"

        return self._select_all(q)

    def get_article(self):
        q = "SELECT * FROM nebula_dashboard_content LIMIT 100"

        return self._select_all(q)
