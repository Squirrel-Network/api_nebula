#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from flask import request

from core.utilities.telegram_auth import decode_telegram_jwt, validate_init_data
from core.utilities.token_jwt import decode_jwt


def auth_required(func: typing.Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = request.headers.get("Authorization", "Bearer XX").split()

        if len(data) <= 1 or not decode_jwt(data[1]):
            return ({"error": "not authorized"}, 401)

        return func(*args, **kwargs)

    return wrapper


def auth_telegram(func: typing.Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        validate = validate_init_data(request.headers.get("X-Init-Data", ""))
        token = request.headers.get("Authorization", "Bearer XX").split()

        print(validate)
        print(decode_telegram_jwt(token[1]))

        if not validate or len(token) <= 1 or not decode_telegram_jwt(token[1]):
            return ({"error": "not authorized"}, 401)

        return func(*args, **kwargs, init_data=validate)

    return wrapper
