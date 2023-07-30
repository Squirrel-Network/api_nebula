#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import dataclasses
import hashlib
import hmac
import urllib.parse

from fastapi import Header, HTTPException
import jwt
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidIssuedAtError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)

from config import Session


@dataclasses.dataclass
class InitDataModel:
    query_id: str
    user: dict
    auth_date: int


def init_data_to_dict(data: str) -> dict:
    return {k: v for k, v in (x.split("=") for x in data.split("&"))}


def validate_init_data(data: str) -> InitDataModel | None:
    try:
        init_data = init_data_to_dict(urllib.parse.unquote(data))

        init_hash = init_data.pop("hash")

        content = "\n".join(
            [f"{k}={v}" for k, v in dict(sorted(init_data.items())).items()]
        )

        secret_key = hmac.new(
            "WebAppData".encode(), Session.config.BOT_TOKEN.encode(), hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            secret_key, content.encode(), hashlib.sha256
        ).hexdigest()

        return InitDataModel(**init_data) if calculated_hash == init_hash else None
    except (ValueError, KeyError):
        return None


def decode_telegram_jwt(token: str) -> bool:
    try:
        return bool(
            jwt.decode(token, Session.config.TELEGRAM_SECRET, algorithms=["HS256"])
        )
    except (
        InvalidTokenError,
        DecodeError,
        InvalidSignatureError,
        ExpiredSignatureError,
        InvalidIssuedAtError,
        InvalidKeyError,
        InvalidAlgorithmError,
        MissingRequiredClaimError,
    ):
        return False


async def validate_telegram(
    init_data: str = Header(alias="X-Init-Data"),
    token_jwt: str = Header(alias="Authorization"),
) -> InitDataModel:
    try:
        validate = validate_init_data(init_data)
        token = token_jwt.split("Bearer ")[1]

        if not validate or not decode_telegram_jwt(token):
            raise HTTPException(status_code=401, detail="Not authorized")

        return validate
    except IndexError:
        raise HTTPException(status_code=401, detail="Not authorized")
