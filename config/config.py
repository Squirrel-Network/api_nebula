#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import os
import typing

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)

LIST_ENV = {
    "HOST": "MYSQL_HOST",
    "PORT": "MYSQL_PORT",
    "USER": "MYSQL_USER",
    "PASSWORD": "MYSQL_PASSWORD",
    "DBNAME": "MYSQL_DBNAME",
    "TOKEN": "TOKEN",
    "SECRET": "SECRET",
    "BOT_TOKEN": "BOT_TOKEN",
    "TELEGRAM_SECRET": "TELEGRAM_SECRET",
    "STAFF_GROUP_ID": "STAFF_GROUP_ID",
}


class MyCustomSource(EnvSettingsSource):
    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: typing.Any,
        value_is_complex: bool,
    ) -> typing.Any:
        if v := os.environ.get(LIST_ENV.get(field_name) or ""):
            return v
        return value


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
    STAFF_GROUP_ID: int

    # Telegram settings
    BOT_TOKEN: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)
