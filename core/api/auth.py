#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import hashlib
import hmac

from flasgger import swag_from
from flask import Blueprint, request

from config import Session
from core.utilities.token_jwt import TokenJwt, encode_jwt
from core.utilities.functions import parse_init_data

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
    init_data, hash_key = parse_init_data(request.json.get("initData", ""))
    secret_key = hmac.new(
        Session.config.BOT_TOKEN.encode("utf-8"),
        "WebAppData".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    init_data_hash = hmac.new(
        secret_key.encode("utf-8"), init_data.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    print(init_data_hash == hash_key)
    print(init_data, hash_key)
