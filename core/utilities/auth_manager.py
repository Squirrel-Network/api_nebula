#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from functools import wraps

import jwt
from flask import Flask, request


class _Auth:
    def init_app(self, app: Flask):
        self.app = app

    def _discover_token(self):
        """
        Search for token in Authorization header as bearer token or in token query string parameter
        """
        auth_header = request.headers.get("authorization", None)
        if auth_header:
            header_segments = [s for s in auth_header.split(" ") if s]
            if (
                len(header_segments) >= 2
                and header_segments[0].lower() == "bearer"
                and header_segments[1]
            ):
                return header_segments[1]
        return request.args.get("token", None)

    def validate_token(self, token):
        data = None
        decode_config = {
            "algorithms": ["HS256"],
        }
        try:
            data = jwt.decode(token, self.app.config["SECRET"], **decode_config)
        except Exception as e:
            self.app.logger.warning("Invalid token: %s", e)

        return data

    def auth_required(self):
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):

                token = self._discover_token()

                token_data = self.validate_token(token) if token else None

                if not token_data:
                    return ({"error": "not authorized"}, 401)

                return fn(*args, **kwargs)

            return decorator

        return wrapper


auth = _Auth()
