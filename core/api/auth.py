#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from fastapi import APIRouter, HTTPException

from config import Session
from core.responses.auth import (
    AuthResponse,
    ErrorMissingToken,
    ErrorNotAuthorized,
    TokenPayload,
)
from core.utilities.token_jwt import TokenJwt, encode_jwt

auth = APIRouter(prefix="/authenticate", tags=["authentication"])


@auth.post(
    "/",
    summary="Authenticates user via token",
    description="Authenticates user via token",
    responses={
        200: {"model": AuthResponse, "description": "Authentication OK"},
        400: {"model": ErrorMissingToken, "description": "Bad Request"},
        403: {"model": ErrorNotAuthorized, "description": "Invalid auth token"},
    },
)
def authenticate(token_payload: TokenPayload):
    token = token_payload.token

    if not token:
        raise HTTPException(status_code=400, detail="Missing token")

    allowed_tokens = Session.config.TOKEN.split(",")

    if token not in allowed_tokens:
        raise HTTPException(status_code=403, detail="Not authorized")

    token_jwt = TokenJwt(True)

    return AuthResponse(token=encode_jwt(token_jwt))
