#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import hashlib
import hmac
import urllib.parse

from flasgger import swag_from
from flask import Blueprint, request

from config import Session
from core.utilities.functions import parse_init_data
from core.utilities.token_jwt import TokenJwt, encode_jwt

auth = Blueprint("auth", __name__)


@swag_from("../../openapi/auth.yaml")
@auth.route("/authenticate", methods=["POST"])
def authenticate():
    token = None

    if request.json:
        token = request.json.get("token", None)
    elif request.form:
        token = request.form.get("token", None)

    if not token:
        return ({"error": "missing token"}, 400)

    if not token in Session.config.TOKEN.split(","):
        return ({"error": "not authorized"}, 403)

    token_jwt = TokenJwt(True)

    return {"token": encode_jwt(token_jwt)}


@auth.route("/login", methods=["POST"])
def login():
    print(request.json)
