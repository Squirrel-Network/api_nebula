#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import dataclasses
import datetime

import jwt
from fastapi import Header, HTTPException
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
class TokenJwt:
    auth: bool
    exp: int = None
    iss: str = "nebula_api"

    def to_dict(self):
        return dict(auth=self.auth, exp=self.exp, iss=self.iss)


def encode_jwt(payload: TokenJwt) -> str:
    payload.exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        minutes=Session.config.TOKEN_DURATION_MINUTES
    )

    return jwt.encode(payload.to_dict(), Session.config.SECRET, algorithm="HS256")


def decode_jwt(token: str) -> TokenJwt | None:
    try:
        result = jwt.decode(token, Session.config.SECRET, algorithms=["HS256"])

        return TokenJwt(**result)
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
        return None


async def validate_token(access_token: str = Header(alias="Authorization")) -> TokenJwt:
    try:
        token = decode_jwt(access_token.split("Bearer ")[1])

        if not token:
            raise HTTPException(status_code=401, detail="Not authorized")

        return token
    except IndexError:
        raise HTTPException(status_code=401, detail="Not authorized")
