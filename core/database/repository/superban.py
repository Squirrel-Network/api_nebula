#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection
from pypika import Query, Table, Order, functions as fn

superban = Table("superban_table")


class SuperbanRepository(Connection):
    def get_by_id(self, user_id: int):
        q = "SELECT * FROM superban_table WHERE user_id = %s"

        return self._select(q, (user_id,))

    def get_all(self, start: int, end: int):
        q = "SELECT * FROM superban_table LIMIT %s,%s"

        return self._select_all(q, (start, end))

    def get_last_super_banned(self):
        q = "SELECT * FROM superban_table WHERE user_date BETWEEN DATE_SUB(NOW(), INTERVAL 15 DAY) AND NOW() ORDER BY user_date DESC LIMIT 8"

        return self._select_all(q)

    def get_first_letter_by_name(self):
        q = "SELECT user_first_name FROM superban_table WHERE user_date BETWEEN DATE_SUB(NOW(), INTERVAL 15 DAY) AND NOW() ORDER BY user_date DESC LIMIT 8"

        return self._select_all(q)

    def get_count_super_banned(self):
        q = "SELECT COUNT(*) AS counter FROM superban_table"

        return self._select(q)

    def add(self, user_id: int, motivation_text: str, user_date: str, id_operator: int):
        q = "INSERT IGNORE INTO superban_table(user_id, motivation_text, user_date, id_operator) VALUES (%s,%s,%s,%s)"

        return self._execute(q, (user_id, motivation_text, user_date, id_operator))

    def get_all(self, **parameters):
        query = Query.from_(superban).select("*")
        query = self._apply_conditions(query, **parameters)
        query = self._apply_order_by(query, **parameters)
        query = self._apply_pagination(query, **parameters)
        q = query.get_sql(quote_char=None)
        print(q)
        return self._select_all(q)

    def count(self, **parameters):
        query = Query.from_(superban).select(fn.Count(1).as_("count"))
        query = self._apply_conditions(query, **parameters)
        q = query.get_sql(quote_char=None)
        print(q)
        return self._select(q)["count"]

    def _apply_pagination(self, query: Query, **parameters):
        if "@start" in parameters:
            query = query.offset(parameters["@start"])
        if "@limit" in parameters:
            query = query.limit(parameters["@limit"])
        return query

    def _apply_order_by(self, query: Query, **parameters):
        valid_order_fields = [
            "id",
            "user_id",
            "motivation_text",
            "user_date",
            "id_operator",
        ]
        order_by = parameters.get("@order_field", None)

        if order_by in valid_order_fields:
            order_dir = parameters.get("@order_dir", "").lower()
            order_dir = Order.desc if order_dir == "desc" else Order.asc
            query = query.orderby(order_by, order=order_dir)

        return query

    def _apply_conditions(self, query: Query, **parameters):
        user_id = parameters.get("user_id", None)
        if user_id:
            query = query.where(superban.user_id.like("%{0}%".format(user_id)))
        motivation_text = parameters.get("motivation_text", None)
        if motivation_text:
            query = query.where(
                superban.motivation_text.like("%{0}%".format(motivation_text))
            )
        id_operator = parameters.get("id_operator", None)
        if id_operator:
            query = query.where(superban.id_operator.like("%{0}%".format(id_operator)))
        return query
