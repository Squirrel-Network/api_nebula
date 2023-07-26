#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import re

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import Session
from core.database import models

HAS_SNAKE_CASE: str = "^[a-z]+(_[a-z]+)*$"


def is_snake_case(data: str) -> bool:
    return bool(re.match(HAS_SNAKE_CASE, data))


def init_db(app: FastAPI):
    conf = Session.config

    register_tortoise(
        app,
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": conf.HOST,
                        "port": conf.PORT,
                        "user": conf.USER,
                        "password": conf.PASSWORD,
                        "database": conf.DBNAME,
                    },
                }
            },
            "apps": {
                "models": {
                    "models": list(
                        map(
                            lambda x: f"core.database.models.{x}",
                            filter(is_snake_case, dir(models)),
                        )
                    ),
                    "default_connection": "default",
                }
            },
            "timezone": "Europe/Rome",
        },
        generate_schemas=True,
    )
