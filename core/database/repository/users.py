#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core.database.db_connect import Connection
from pypika import Query, Table, Order, functions as fn

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

    def get_all(self, **parameters):
        query = Query.from_(users).select("*")
        query = self._apply_conditions(query, **parameters)
        query = self._apply_order_by(query, **parameters)
        query = self._apply_pagination(query, **parameters)
        q = query.get_sql(quote_char=None)
        print(q)
        return self._selectAll(q)

    def count(self, **parameters):
        query = Query.from_(users).select(fn.Count(1).as_('count'))
        query = self._apply_conditions(query, **parameters)
        q = query.get_sql(quote_char=None)
        print(q)
        return self._select(q)['count']

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

    def _apply_pagination(self, query: Query, **parameters):
        if '@start' in parameters:
            query = query.offset(parameters['@start'])
        if '@limit' in parameters:
            query = query.limit(parameters['@limit'])
        return query

    def _apply_order_by(self, query: Query, **parameters):
        valid_order_fields = ['id', 'tg_username' , 'tg_id', 'created_at', 'updated_at']
        order_by = parameters.get('@order_field', None)


        if order_by in valid_order_fields:
            order_dir = parameters.get('@order_dir', '').lower()
            print(order_dir)
            order_dir = Order.desc if order_dir == 'desc' else Order.asc
            print(order_dir)
            print(order_by)
            query = query.orderby(order_by, order=order_dir)

        return query

    def _apply_conditions(self, query: Query, **parameters):
        username = parameters.get('tg_username', None)
        if username:
            query = query.where(users.tg_username.like('%{0}%'.format(username)))
        return query