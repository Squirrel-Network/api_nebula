#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection
from pypika import Query, Table, Order, functions as fn

users = Table("users")


class UserRepository(Connection):
    def get_by_id(self, tg_id: int):
        q = "SELECT * FROM users WHERE tg_id = %s"

        return self._select(q, (tg_id,))

    def get_by_username(self, tg_username: str):
        q = "SELECT * FROM users WHERE tg_username = %s"

        return self._select(q, (tg_username,))

    def get_all(self, **parameters):
        query = Query.from_(users).select("*")
        query = self._apply_conditions(query, **parameters)
        query = self._apply_order_by(query, **parameters)
        query = self._apply_pagination(query, **parameters)
        q = query.get_sql(quote_char=None)
        print(q)
        return self._select_all(q)

    def count(self, **parameters):
        query = Query.from_(users).select(fn.Count(1).as_("count"))
        query = self._apply_conditions(query, **parameters)
        q = query.get_sql(quote_char=None)
        print(q)
        return self._select(q)["count"]

    def add(self, tg_id: int, tg_username: str, warn_count: int):
        q = "INSERT INTO users (tg_id, tg_username, warn_count) VALUES (%s,%s,%s)"

        return self._execute(q, (tg_id, tg_username, warn_count))

    def update(self, tg_username: str, tg_id: int):
        q = "UPDATE users SET tg_username = %s WHERE tg_id = %s"

        return self._execute(q, (tg_username, tg_id))

    def delete_user(self, tg_id: int):
        q = "DELETE FROM users WHERE tg_id = %s"

        return self._execute(q, (tg_id,))

    def _apply_pagination(self, query: Query, **parameters):
        if "@start" in parameters:
            query = query.offset(parameters["@start"])
        if "@limit" in parameters:
            query = query.limit(parameters["@limit"])
        return query

    def _apply_order_by(self, query: Query, **parameters):
        valid_order_fields = ["id", "tg_username", "tg_id", "created_at", "updated_at"]
        order_by = parameters.get("@order_field", None)

        if order_by in valid_order_fields:
            order_dir = parameters.get("@order_dir", "").lower()
            print(order_dir)
            order_dir = Order.desc if order_dir == "desc" else Order.asc
            print(order_dir)
            print(order_by)
            query = query.orderby(order_by, order=order_dir)

        return query

    def _apply_conditions(self, query: Query, **parameters):
        username = parameters.get("tg_username", None)
        if username:
            query = query.where(users.tg_username.like("%{0}%".format(username)))
        return query

    def get_count_users(self):
        q = "SELECT COUNT(*) AS counter FROM users"

        return self._select(q)

    def get_sn_staff(self):
        q = "SELECT * FROM nebula_dashboard_staff LIMIT 50"

        return self._select_all(q)
