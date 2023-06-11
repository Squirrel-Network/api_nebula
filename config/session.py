#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pymysqlpool import ConnectionPool

from config import Config


class Session:
    config: Config
    db_pool: ConnectionPool
