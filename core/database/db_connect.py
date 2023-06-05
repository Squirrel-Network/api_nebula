#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import pymysql
from config import Session


class Connection:
    def __init__(self):
        self.con = pymysql.connect(
            host=Session.config.HOST,
            port=Session.config.PORT,
            user=Session.config.USER,
            password=Session.config.PASSWORD,
            db=Session.config.DBNAME,
            autocommit=True,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cur = self.con.cursor()

    def _select(self, sql, args=None):
        self.cur.execute(sql, args)
        self.sel = self.cur.fetchone()
        self.cur.close()
        self.con.close()
        return self.sel

    def _selectAll(self, sql, args=None):
        print(args)
        self.cur.execute(sql, args)
        self.sel = self.cur.fetchall()
        self.cur.close()
        self.con.close()
        return self.sel

    def _insert(self, sql, args=None):
        self.ins = self.cur.executemany(sql, args)
        return self.ins

    def _update(self, sql, args=None):
        self.upd = self.cur.executemany(sql, args)
        return self.upd

    def _delete(self, sql, args=None):
        self.delete = self.cur.executemany(sql, args)
        return self.delete
