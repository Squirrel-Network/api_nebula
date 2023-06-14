#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseSettings

LIST_ENV = (
    ("HOST", "MYSQL_HOST"),
    ("PORT", "MYSQL_PORT"),
    ("USER", "MYSQL_USER"),
    ("PASSWORD", "MYSQL_PASSWORD"),
    ("DBNAME", "MYSQL_DBNAME"),
    ("TOKEN", "TOKEN"),
    ("SECRET", "SECRET"),
    ("BOT_TOKEN", "BOT_TOKEN"),
    ("TELEGRAM_SECRET", "TELEGRAM_SECRET"),
)


class Config(BaseSettings):
    # Database settings
    HOST: str = "localhost"
    PORT: int = 3306
    USER: str
    PASSWORD: str
    DBNAME: str

    # App settings
    DEBUG: bool = False
    TOKEN: str
    SECRET: str
    TOKEN_DURATION_MINUTES: int = 10
    PAGE_SIZE_DEFAULT: int = 50
    PAGE_SIZE_MAX: int = 1000
    TELEGRAM_SECRET: str

    # Telegram settings
    BOT_TOKEN: str

    class Config:
        fields = {name: {"env": env} for name, env in LIST_ENV}
