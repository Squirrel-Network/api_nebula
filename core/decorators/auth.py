#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from flask import request

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
