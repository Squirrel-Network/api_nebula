#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import hashlib
import hmac
import typing
import urllib.parse

from flask import request

from config import Session
from core.utilities.functions import parse_init_data
from core.utilities.token_jwt import decode_jwt


def auth_required(func: typing.Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = request.headers.get("authorization", "Bearer XX").split()
        token = decode_jwt(data[1])

        if not token:
            return ({"error": "not authorized"}, 401)

        return func(*args, **kwargs)

    return wrapper


def auth_telegram(func: typing.Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = urllib.parse.unquote(request.headers.get("X-Init-Data", ""))
        init_data, hash_key = parse_init_data(data)

        if not init_data or not hash_key:
            return ({"error": "not authorized"}, 401)

        secret_key = hmac.new(
            "WebAppData".encode(), Session.config.BOT_TOKEN.encode(), hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            secret_key, init_data.encode(), hashlib.sha256
        ).hexdigest()

        if hash_key != calculated_hash:
            return ({"error": "not authorized"}, 401)

        return func(*args, **kwargs)

    return wrapper
